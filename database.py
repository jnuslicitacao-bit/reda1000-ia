from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./redacao_saas.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Usuário (Controle de créditos e gamificação básica)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    plan_type = Column(String, default="FREE") # FREE ou PREMIUM
    credits = Column(Integer, default=3) # Créditos para o plano free
    xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)

# Modelo de Temas de Redação
class Theme(Base):
    __tablename__ = "themes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    context = Column(Text, nullable=False)
    banca = Column(String, default="ENEM")

# Modelo de Redações e Correções da IA
class Essay(Base):
    __tablename__ = "essays"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    theme_id = Column(Integer, ForeignKey("themes.id"))
    content = Column(Text, nullable=False)
    final_score = Column(Integer, nullable=True)
    ai_feedback = Column(JSON, nullable=True) # Salva o JSON gerado pela IA
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_create_all=Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()