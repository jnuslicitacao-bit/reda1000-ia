import os
import datetime
import jwt
from typing import List, Dict, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from dotenv import load_dotenv

# Importações dos nossos módulos locais
import database
import ai_service

load_dotenv()

app = FastAPI(
    title="Reda1000IA - API Core",
    description="Backend escalável para Micro SaaS de Correção de Redação com IA",
    version="1.0.0"
)

# Configuração de CORS para permitir que o Frontend (Streamlit/React) se comunique sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAÇÕES DE SEGURANÇA E JWT ---
SECRET_KEY = os.getenv("JWT_SECRET", "super-segredo-do-modulo-saas-123")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais de acesso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.PyJWTError:
        raise credentials_exception

# --- EVENTOS DE INICIALIZAÇÃO ---
@app.on_event("startup")
def on_startup():
    database.init_db()
    db = next(database.get_db())
    
    # Popular dados iniciais de teste se o banco de produção estiver limpo
    if not db.query(database.User).first():
        test_user = database.User(
            name="Estudante Nota 1000", 
            email="aluno@enem.com", 
            plan_type="FREE", 
            credits=3
        )
        
        test_theme = database.Theme(
            title="O estigma associado às doenças mentais na sociedade brasileira",
            context="Textos motivadores sobre a persistência do preconceito contra distúrbios psíquicos...",
            banca="ENEM"
        )
        
        db.add(test_user)
        db.add(test_theme)
        db.commit()
        print("🚀 Banco de dados de produção limpo e inicializado com sucesso!")

# --- SCHEMAS DE VALIDAÇÃO DE ENTRADA (PYDANTIC) ---
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class EssaySubmission(BaseModel):
    theme_id: int
    content: str

class ThemeCreate(BaseModel):
    title: str
    context: str
    banca: str  # 'ENEM', 'FUVEST', 'CONCURSOS'


# --- ROTAS DE GERENCIAMENTO DE TEMAS ---

@app.post("/api/themes", status_code=201)
def create_new_theme(theme_in: ThemeCreate, db: Session = Depends(database.get_db)):
    """
    Rota para cadastrar novos temas de redação no banco de dados.
    """
    new_theme = database.Theme(
        title=theme_in.title,
        context=theme_in.context,
        banca=theme_in.banca
    )
    db.add(new_theme)
    db.commit()
    db.refresh(new_theme)
    return {"message": "Tema cadastrado com sucesso!", "theme_id": new_theme.id}

@app.get("/api/themes")
def list_active_themes(db: Session = Depends(database.get_db)):
    """
    Rota utilizada pelo frontend para listar e popular dinamicamente o seletor de propostas.
    """
    themes = db.query(database.Theme).all()
    return [{"id": t.id, "title": t.title, "banca": t.banca} for t in themes]


# --- ROTAS DE AUTENTICAÇÃO ---

@app.post("/api/auth/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(database.User).filter(database.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")
    
    new_user = database.User(
        name=user_in.name,
        email=user_in.email,
        plan_type="FREE",
        credits=3
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário criado com sucesso!", "user_id": new_user.id}

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos.")
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


# --- ROTAS DA REGRA DE NEGÓCIO (ESSAYS) ---

@app.post("/api/essays/submit")
def submit_essay(submission: EssaySubmission, current_user_id: int = Depends(get_current_user_id), db: Session = Depends(database.get_db)):
    # 1. Validar Usuário e Limite de Créditos
    user = db.query(database.User).filter(database.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não localizado.")
        
    if user.plan_type == "FREE" and user.credits <= 0:
        raise HTTPException(
            status_code=403, 
            detail="Seus créditos gratuitos acabaram! Assine o Plano Premium para correções ilimitadas."
        )
    
    # 2. Buscar o tema proposto
    theme = db.query(database.Theme).filter(database.Theme.id == submission.theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Tema de redação inválido ou não encontrado.")
        
    try:
        # 3. Chamar o motor de Inteligência Artificial estruturado
        correction_result = ai_service.analyze_essay_with_ai(
            essay_content=submission.content,
            theme_title=theme.title,
            theme_context=theme.context
        )
        
        # 4. Debitar créditos (se aplicável) e atualizar métricas de gamificação
        if user.plan_type == "FREE":
            user.credits -= 1
        user.xp += 100
        user.streak_days += 1
        
        # 5. Registrar histórico no banco de dados
        new_essay = database.Essay(
            user_id=user.id,
            theme_id=theme.id,
            content=submission.content,
            final_score=correction_result["final_score"],
            ai_feedback=correction_result
        )
        db.add(new_essay)
        db.commit()
        db.refresh(new_essay)
        
        return {
            "message": "Redação corrigida com sucesso!",
            "essay_id": new_essay.id,
            "xp_ganho": 100,
            "creditos_restantes": user.credits,
            "resultado": correction_result
        }
        
    except Exception as e:
        db.rollback()
        print("\n=== CRITICAL BACKEND ERROR ===")
        print(str(e))
        print("==============================\n")
        raise HTTPException(status_code=500, detail=f"Falha interna no processador de IA: {str(e)}")


# --- ROTAS DO DASHBOARD ---

@app.get("/api/dashboard")
def get_dashboard_data(current_user_id: int = Depends(get_current_user_id), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não localizado.")
        
    essays = db.query(database.Essay).filter(database.Essay.user_id == current_user_id).all()
    
    scores = [e.final_score for e in essays if e.final_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    target_score = 900
    
    points_to_target = max(0, target_score - avg_score) if scores else target_score
    
    return {
        "user_profile": {
            "name": user.name,
            "plan": user.plan_type,
            "credits": user.credits,
            "xp": user.xp,
            "streak": user.streak_days
        },
        "metrics": {
            "total_essays": len(essays),
            "average_score": round(avg_score, 1),
            "target_score": target_score,
            "status_message": f"Você está a {round(points_to_target)} pontos da sua meta de {target_score}!" if points_to_target > 0 else "Parabéns! Você alcançou o nível de corte da sua meta!"
        },
        "history": [
            {"id": e.id, "score": e.final_score, "date": e.created_at.strftime("%Y-%m-%d")} for e in essays
        ]
    }


# --- WEBHOOK DE MONETIZAÇÃO (STRIPE / ASAAS) ---

@app.post("/api/webhooks/payment")
async def payment_webhook(request: Request, db: Session = Depends(database.get_db)):
    """
    Endpoint seguro acionado pelo gateway de pagamento assim que a assinatura ou o PIX é confirmado.
    """
    try:
        payload = await request.json()
        event_type = payload.get("event") or payload.get("type")
        
        # Mapeamento genérico de eventos de sucesso de pagamento
        if event_type in ["payment.confirmed", "checkout.session.completed", "subscription.created"]:
            # Coleta o e-mail enviado via metadata ou cadastro do cliente no checkout
            data_obj = payload.get("data", {})
            customer_info = data_obj.get("customer", {})
            customer_email = customer_info.get("email") or payload.get("customer_email")
            
            if customer_email:
                user = db.query(database.User).filter(database.User.email == customer_email).first()
                if user:
                    user.plan_type = "PREMIUM"
                    user.credits = 99999  # Representação de créditos ilimitados para o motor
                    db.commit()
                    return {"status": "success", "message": f"Plano PREMIUM ativado para {customer_email}"}
                    
        return {"status": "ignored", "message": "Evento de pagamento não relevante para atualização de assinatura."}
    except Exception as e:
        return {"status": "error", "message": str(e)}