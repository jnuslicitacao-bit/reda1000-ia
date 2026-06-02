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

import database
import ai_service

load_dotenv()

app = FastAPI(
    title="Reda1000IA - API Core",
    description="Backend corrigido contra quebras de usuários antigos",
    version="1.2.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.on_event("startup")
def on_startup():
    database.init_db()
    db = next(database.get_db())
    if not db.query(database.User).first():
        test_user = database.User(
            name="Estudante Nota 1000", 
            email="aluno@enem.com", 
            plan_type="FREE", 
            credits=3,
            referral_code="REDA1K",
            xp=0,
            streak_days=0
        )
        test_theme = database.Theme(
            title="O estigma associado às doenças mentais na sociedade brasileira",
            context="Textos motivadores sobre a persistência do preconceito contra distúrbios psíquicos...",
            banca="ENEM"
        )
        db.add(test_user)
        db.add(test_theme)
        db.commit()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    referred_by_code: Optional[str] = None

class EssaySubmission(BaseModel):
    theme_id: int
    content: str

class ThemeCreate(BaseModel):
    title: str
    context: str
    banca: str 

@app.post("/api/auth/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(database.User).filter(database.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")
    
    new_user = database.User(
        name=user_in.name,
        email=user_in.email,
        plan_type="FREE",
        credits=3,
        referral_code=generate_referral_code(),
        xp=0,
        streak_days=0
    )
    
    if user_in.referred_by_code:
        referrer = db.query(database.User).filter(database.User.referral_code == user_in.referred_by_code.upper()).first()
        if referrer:
            current_credits = referrer.credits if referrer.credits is not None else 0
            referrer.credits = current_credits + 1
            
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

@app.post("/api/essays/submit")
def submit_essay(submission: EssaySubmission, current_user_id: int = Depends(get_current_user_id), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não localizado.")
        
    user_credits = user.credits if user.credits is not None else 0
    if user.plan_type == "FREE" and user_credits <= 0:
        raise HTTPException(
            status_code=403, 
            detail="Seus créditos acabaram! Indique amigos para ganhar +1 crédito ou mude para o PREMIUM."
        )
    
    theme = db.query(database.Theme).filter(database.Theme.id == submission.theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Tema de redação inválido.")
        
    try:
        correction_result = ai_service.analyze_essay_with_ai(
            essay_content=submission.content,
            theme_title=theme.title,
            theme_context=theme.context
        )
        
        if user.plan_type == "FREE":
            user.credits = max(0, user_credits - 1)
            
        user.xp = (user.xp if user.xp is not None else 0) + 100
        user.streak_days = (user.streak_days if user.streak_days is not None else 0) + 1
        
        new_essay = database.Essay(
            user_id=user.id,
            theme_id=theme.id,
            content=submission.content,
            final_score=correction_result["final_score"],
            ai_feedback=correction_result
        )
        db.add(new_essay)
        db.commit()
        return {
            "message": "Redação corrigida com sucesso!",
            "resultado": correction_result
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro no motor de IA: {str(e)}")

@app.get("/api/dashboard")
def get_dashboard_data(current_user_id: int = Depends(get_current_user_id), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não localizado.")
        
    # Tratamento retroativo para evitar erros 500 em contas antigas do banco
    if not user.referral_code:
        user.referral_code = generate_referral_code()
        db.commit()
    if user.xp is None:
        user.xp = 0
        db.commit()
    if user.streak_days is None:
        user.streak_days = 0
        db.commit()
    if user.credits is None:
        user.credits = 3 if user.plan_type == "FREE" else 99999
        db.commit()

    essays = db.query(database.Essay).filter(database.Essay.user_id == current_user_id).order_by(database.Essay.created_at.asc()).all()
    scores = [e.final_score for e in essays if e.final_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    share_text = "Estou treinando minha escrita no Reda1000IA!"
    if len(scores) >= 2:
        if (scores[-1] - scores[0]) > 0:
            share_text = f"🔥 Sensacional! Saí de {scores[0]} para {scores[-1]} pontos na redação usando o Reda1000IA!"
        else:
            share_text = f"🎯 Tirei {scores[-1]} na minha última redação do Reda1000IA! Rumo à nota máxima!"

    return {
        "user_profile": {
            "name": user.name if user.name else "Estudante",
            "plan": user.plan_type if user.plan_type else "FREE",
            "credits": user.credits,
            "xp": user.xp,
            "streak": user.streak_days,
            "my_referral_code": user.referral_code
        },
        "metrics": {
            "total_essays": len(essays),
            "average_score": round(avg_score, 1),
            "target_score": 900,
            "status_message": f"Você está a {round(max(0, 900 - avg_score))} pontos da meta."
        },
        "share_marketing": {
            "copy_text": share_text
        },
        "history": [
            {"id": e.id, "score": e.final_score, "date": e.created_at.strftime("%Y-%m-%d")} for e in essays
        ]
    }

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
                    user.credits = 99999
                    db.commit()
                    return {"status": "success"}
        return {"status": "ignored"}
    except:
        return {"status": "error"}