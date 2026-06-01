import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CompetenceScore(BaseModel):
    score: int
    feedback: str

# Mudamos de Dict para um objeto fixo contendo as 5 competências do ENEM
class EnemCompetences(BaseModel):
    c1: CompetenceScore # Domínio da norma culta
    c2: CompetenceScore # Compreensão do tema e aplicação das áreas de conhecimento
    c3: CompetenceScore # Seleção, relação, organização e interpretação de informações
    c4: CompetenceScore # Demonstração de conhecimento dos mecanismos linguísticos (coesão)
    c5: CompetenceScore # Elaboração de proposta de intervenção

class MicroCorrection(BaseModel):
    original_text: str
    corrected_text: str
    error_type: str
    explanation: str
    micro_lesson: str

class EvolutionPlan(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    next_steps: str
    recommended_reading: str

class EssayCorrectionSchema(BaseModel):
    final_score: int
    competences: EnemCompetences # Agora usa a classe fixa ao invés de Dict
    corrections: List[MicroCorrection]
    evolution_plan: EvolutionPlan

def analyze_essay_with_ai(essay_content: str, theme_title: str, theme_context: str) -> dict:
    system_prompt = (
        "Você é uma professora de redação especialista no ENEM e concursos públicos. "
        "Sua correção deve ser extremamente didática, humana, empática e cirúrgica. "
        "Avalie as 5 competências do ENEM (0 a 200 cada). Identifique desvios gramaticais, "
        "reestruture trechos problemáticos e forneça microaulas práticas para cada erro."
    )
    
    user_prompt = f"""
    Tema da Redação: {theme_title}
    Textos de Apoio: {theme_context}
    
    Texto do Aluno:
    \"\"\"
    {essay_content}
    \"\"\"
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=EssayCorrectionSchema,
        temperature=0.3
    )
    
    return response.choices[0].message.parsed.model_dump()