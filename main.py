import os
import datetime
import jwt
import random
import string
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
    description="Backend com motor de crescimento viral e monetização por planos",
    version="1.2.0"
)

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

# --- FUNÇÃO AUXILIAR PARA GERAR CÓDIGO DE REFERRAL ---
def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- EVENTOS DE INICIALIZAÇÃO ---
@app.on_event("startup")
def on_startup():
    database.init_db()
    db = next(database.get_db())
    
    # Garante um utilizador de testes com código de referral limpo
    if not db.query(database.User).first():
        test_user = database.User(
            name="Estudante Nota 1000", 
            email="aluno@enem.com", 
            plan_type="FREE", 
            credits=3,
            referral_code="REDA1K"
        )
        
        test_theme = database.Theme(
            title="O estigma associado às doenças mentais na sociedade brasileira",
            context="Textos motivadores sobre a persistência do preconceito contra distúrbios psíquicos...",
            banca="ENEM"
        )
        
        db.add(test_user)
        db.add(test_theme)
        db.commit()
        print("🚀 Banco de dados inicializado com sucesso!")

# --- SCHEMAS DE VALIDAÇÃO (PYDANTIC) ---
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    referred_by_code: Optional[str] = None  # Código de quem indicou este novo aluno

class EssaySubmission(BaseModel):
    theme_id: int
    content: str

class ThemeCreate(BaseModel):
    title: str
    context: str
    banca: str 


# --- ROTAS DE AUTENTICAÇÃO & CRESCIMENTO (REGISTRATION) ---

@app.post("/api/auth/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(database.User).filter(database.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")
    
    # 1. Criação do novo utilizador com os 3 créditos do Plano Gratuito
    new_user = database.User(
        name=user_in.name,
        email=user_in.email,
        plan_type="FREE",
        credits=3,
        referral_code=generate_referral_code()
    )
    
    # 2. SISTEMA DE GANHO EXTRA POR INDICAÇÃO (LOOP VIRAL)
    if user_in.referred_by_code:
        referrer = db.query(database.User).filter(database.User.referral_code == user_in.referred_by_code.upper()).first()
        if referrer:
            referrer.credits += 1  # Dá +1 correção bónus para o amigo que indicou
            print(f"🎉 Bónus de indicação aplicado! {referrer.name} ganhou +1 crédito.")
            
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


# --- ROTAS DE GERENCIAMENTO DE TEMAS ---

@app.post("/api/themes", status_code=201)
def create_new_theme(theme_in: ThemeCreate, db: Session = Depends(database.get_db)):
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
    themes = db.query(database.Theme).all()
    return [{"id": t.id, "title": t.title, "banca": t.banca} for t in themes]


# --- SUBMISSÃO DE REDAÇÃO COM REGRAS DE PLANO ---

@app.post("/api/essays/submit")
def submit_essay(submission: EssaySubmission, current_user_id: int = Depends(get_current_user_id), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não localizado.")
        
    # TRAVA DO PLANO GRATUITO
    if user.plan_type == "FREE" and user.credits <= 0:
        raise HTTPException(
            status_code=403, 
            detail="Seus créditos acabaram! Indique amigos para ganhar +1 crédito ou mude para o PREMIUM para ter correções ilimitadas."
        )
    
    theme = db.query(database.Theme).filter(database.Theme.id == submission.theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Tema de redação inválido.")
        
    try:
        # Chamada do modelo GPT
        correction_result = ai_service.analyze_essay_with_ai(
            essay_content=submission.content,
            theme_title=theme.title,
            theme_context=theme.context
        )
        
        # Debita crédito se for gratuito. Premium é ilimitado.
        if user.plan_type == "FREE":
            user.credits -= 1
            
        user.xp += 100
        user.streak_days += 1
        
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
            "creditos_restantes": user.credits,
            "resultado": correction_result
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno no motor de IA: {str(e)}")


# --- DASHBOARD INTELIGENTE COM CÁLCULO DE EVOLUÇÃO SOCIAL ---

@app.get("/api/dashboard")
def get_dashboard_data(current_user_id: int = Depends(get_current_user_id), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não localizado.")
        
    essays = db.query(database.Essay).filter(database.Essay.user_id == current_user_id).order_by(database.Essay.created_at.asc()).all()
    
    scores = [e.final_score for e in essays if e.final_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    target_score = 900
    
    # GERAÇÃO DA COPY DE EVOLUÇÃO COMPARTILHÁVEL
    share_text = "Estou treinando minha escrita no Reda1000IA!"
    if len(scores) >= 2:
        evolução = scores[-1] - scores[0]
        if evolução > 0:
            share_text = f"🔥 Sensacional! Saí de {scores[0]} para {scores[-1]} pontos na redação usando o tutor inteligente do Reda1000IA! Quem quer o link grátis?"
        else:
            share_text = f"🎯 Acabei de tirar {scores[-1]} na minha última redação do Reda1000IA! Rumo à nota máxima!"

    # Garante que o código de referral do usuário existe (correção retroativa se necessário)
    if not user.referral_code:
        user.referral_code = generate_referral_code()
        db.commit()

    return {
        "user_profile": {
            "name": user.name,
            "plan": user.plan_type,
            "credits": user.credits,
            "xp": user.xp,
            "streak": user.streak_days,
            "my_referral_code": user.referral_code  # Código dele para expor no front
        },
        "metrics": {
            "total_essays": len(essays),
            "average_score": round(avg_score, 1),
            "target_score": target_score,
            "status_message": f"Você está a {round(max(0, target_score - avg_score))} pontos da nota de corte!"
        },
        "share_marketing": {
            "copy_text": share_text
        },
        "history": [
            {"id": e.id, "score": e.final_score, "date": e.created_at.strftime("%Y-%m-%d")} for e in essays
        ]
    }


# --- WEBHOOK DE CONFIRMAÇÃO DE UPGRADE (PREMIUM) ---

@app.post("/api/webhooks/payment")
async def payment_webhook(request: Request, db: Session = Depends(database.get_db)):
    try:
        payload = await request.json()
        event_type = payload.get("event") or payload.get("type")
        
        if event_type in ["payment.confirmed", "checkout.session.completed", "subscription.created"]:
            data_obj = payload.get("data", {})
            customer_info = data_obj.get("customer", {})
            customer_email = customer_info.get("email") or payload.get("customer_email")
            
            if customer_email:
                user = db.query(database.User).filter(database.User.email == customer_email).first()
                if user:
                    user.plan_type = "PREMIUM"
                    user.credits = 99999  # Ativa acesso ilimitado
                    db.commit()
                    return {"status": "success", "message": f"Plano PREMIUM ativado para {customer_email}"}
                    
        return {"status": "ignored"}
    except Exception as e:
        return {"status": "error", "message": str(e)}