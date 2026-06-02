import streamlit as st
import requests
import datetime

# Configuração da página do Streamlit
st.set_page_config(page_title="Reda1000IA - Micro SaaS", page_icon="🚀", layout="wide")

# Lógica inteligente de URL
if "API_BASE_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_BASE_URL"]
else:
    API_BASE_URL = "http://127.0.0.1:8000/api"

# COLE AQUI A URL DIRETA DA SUA LOGO (Hospedada no Imgur, GitHub, etc.)
LOGO_URL = "URL_DA_SUA_IMAGEM_AQUI" 

# Inicializa variáveis de estado de sessão
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- INJEÇÃO DE DESIGN PREMIUM COM LOGO E OTIMIZAÇÃO MOBILE ---
st.markdown(f"""
    <style>
        /* Estilização do fundo */
        .stApp {{
            background: linear-gradient(135deg, #f8f9fc 0%, #e2e8f0 100%);
        }}
        
        /* CONTAINER DA LOGO EM IMAGEM */
        .logo-container {{
            text-align: center;
            padding: 20px 0 0px 0;
            margin: 0 auto;
            max-width: 450px;
        }}
        .logo-img {{
            width: 100%;
            height: auto;
            max-height: 280px;
            object-fit: contain;
        }}
        
        /* CARROSSEL DE PROVA SOCIAL AJUSTADO */
        .ticker-wrapper {{
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 12px 0;
            margin-bottom: 25px;
            border-radius: 50px;
            box-shadow: 0 4px 12px rgba(30, 60, 114, 0.15);
        }}
        .ticker {{
            display: flex;
            white-space: nowrap;
            animation: ticker-animation 55s linear infinite;
        }}
        .ticker-item {{
            color: white;
            padding: 0 45px;
            font-size: 0.95rem;
            font-weight: 500;
        }}
        .ticker-item b {{
            color: #deff9a;
        }}
        @keyframes ticker-animation {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
        
        /* BOX DE URGÊNCIA/ESCASSEZ */
        .urgency-box {{
            background-color: #fff5f5;
            border-left: 5px solid #ff416c;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin: 10px auto 30px auto;
            max-width: 600px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }}
        .urgency-text {{
            color: #c53030;
            font-weight: 700;
            font-size: 1.05rem;
            margin: 0;
        }}
        
        /* REMOÇÃO COMPLETA DO RETÂNGULO VAZIO EM CIMA DO LOGIN */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            justify-content: center;
            border-bottom: none !important;
            padding: 0 !important;
            margin-bottom: -10px !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            border: none !important;
            box-shadow: none !important;
        }}
        .stTabs [data-baseweb="tab-panel"] {{
            padding-top: 0px !important;
            margin-top: 0px !important;
        }}
        
        /* CARD DE LOGIN */
        .login-card {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.06);
            border: 1px solid #edf2f7;
            margin-top: 0px !important;
        }}
        
        /* CENTRALIZAÇÃO E DESIGN DO BOTÃO */
        div.stButton > button:first-child {{
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 14px;
            font-weight: bold;
            width: 100%;
            margin: 20px auto 0 auto; /* Centraliza no eixo do bloco */
            display: block;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }}
        div.stButton > button:first-child:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(30, 60, 114, 0.25);
        }}

        /* OTIMIZAÇÃO RIGOROSA PARA DISPOSITIVOS MÓVEIS (MOBILE) */
        @media (max-width: 768px) {{
            .logo-container {{ max-width: 280px; padding-top: 10px; }}
            .ticker-item {{ padding: 0 15px; font-size: 0.75rem; }}
            .ticker-wrapper {{ border-radius: 20px; padding: 6px 0; margin-bottom: 15px; }}
            .urgency-box {{ padding: 10px; margin-bottom: 20px; }}
            .urgency-text {{ font-size: 0.85rem; }}
            .login-card {{ padding: 20px !important; border-radius: 16px; }}
        }}
    </style>
""", unsafe_allow_html=True)


# --- TELA DE AUTENTICAÇÃO ---
if not st.session_state.logged_in:
    
    # 1. LOGO EM IMAGEM (Substituindo o texto antigo)
    st.markdown(f'''
        <div class="logo-container">
            <img src="{'C:\Users\USER\Desktop\Reda1000IA\logo.png'}" class="logo-img" alt="Reda1000IA Logo">
        </div>
    ''', unsafe_allow_html=True)
    
    # 2. CARROSSEL DE PROVA SOCIAL
    st.markdown('''
        <div class="ticker-wrapper">
            <div class="ticker">
                <div class="ticker-item">🎯 <b>Matheus S.</b> alcançou nota <b>980</b> no ENEM!</div>
                <div class="ticker-item">🚀 <b>Ana Clara</b> subiu de 600 para <b>920</b> em 2 semanas!</div>
                <div class="ticker-item">🔥 <b>João Pedro</b> garantiu <b>940</b> na redação do TJ-SP!</div>
                <div class="ticker-item">✨ <b>Carla M.</b> nota <b>900+</b> usando a Reda1000IA</div>
                <div class="ticker-item">🎯 <b>Lucas F.</b> nota <b>960</b> com nosso método!</div>
                <div class="ticker-item">🚀 <b>Beatriz H.</b> nota <b>940</b> na Fuvest!</div>
                <div class="ticker-item">✨ <b>Aline A.</b> nota <b>758+</b> usando a Reda1000IA</div>
                <div class="ticker-item">🎯 <b>Isabella G.</b> subiu de 420 para <b>910</b> com nosso método!</div>
                <div class="ticker-item">🚀 <b>Beatriz A.</b> nota <b>840</b> na Fuvest!</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # 3. CONTEXTO DE CONVERSÃO (URGÊNCIA)
    st.markdown('''
        <div class="urgency-box">
            <p class="urgency-text">
                ⚠️ RESTAM APENAS <b>14 VAGAS</b> COM ACESSO GRATUITO NESTA SEMANA.<br>
                <small>A oferta de lançamento encerra hoje às 23:59.</small>
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Grid de Centralização
    _, col_central, _ = st.columns([1, 1.6, 1])
    
    with col_central:
        tab_login, tab_cad = st.tabs(["🔒 Entrar", "✨ Criar Conta Grátis"])
        
        with tab_login:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            u_login = st.text_input("E-mail", key="u_log", placeholder="estudante@email.com")
            p_login = st.text_input("Senha", type="password", key="p_log", placeholder="Digite sua senha")
            
            if st.button("ACESSAR MINHA ÁREA", type="primary", key="btn_l"):
                payload = {"username": u_login, "password": p_login}
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", data=payload)
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha inválidos.")
                except:
                    st.error("⚠️ Servidor offline. Tente em instantes.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab_cad:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            n_cad = st.text_input("Nome", placeholder="Seu nome completo")
            e_cad = st.text_input("E-mail", placeholder="seu.email@escola.com")
            s_cad = st.text_input("Senha", type="password", placeholder="Crie uma senha forte")
            
            if st.button("GARANTIR MINHA VAGA AGORA", key="btn_c"):
                if n_cad and e_cad and s_cad:
                    payload = {"name": n_cad, "email": e_cad, "password": s_cad}
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                        if res.status_code == 201:
                            st.success("✨ Conta criada! Volte para a aba 'Entrar'.")
                        else:
                            st.error(res.json().get("detail", "Erro no cadastro."))
                    except:
                        st.error("⚠️ Erro de conexão.")
                else:
                    st.warning("⚠️ Preencha todos os campos.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- ÁREA LOGADA ---
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard", headers=headers)
        if response.status_code == 200:
            dash_data = response.json()
        else:
            st.session_state.logged_in = False
            st.rerun()
    except:
        st.error("Erro ao carregar o painel.")
        st.stop()

    profile = dash_data.get("user_profile", {})
    metrics = dash_data.get("metrics", {})
    
    st.title("📝 Reda1000IA — Área do Aluno")
    
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 2, 1])
    with c1: st.metric("Estudante", profile.get("name"))
    with c2: st.metric("XP", f"{profile.get('xp')}")
    with c3: st.metric("🔥 Ofensiva", f"{profile.get('streak')}d")
    with c4: st.metric("Plano", profile.get("plan"), f"{profile.get('credits')} créditos")
    with c5:
        if st.button("Sair"):
            st.session_state.token = None
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")
    st.subheader("📊 Sua Evolução")
    st.info(metrics.get("status_message"))
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Média das Notas", metrics.get("average_score"))
    m2.metric("Redações Corrigidas", metrics.get("total_essays"))
    m3.metric("Meta", metrics.get("target_score"))
        
    history = dash_data.get("history", [])
    if history:
        st.line_chart([e["score"] for e in history])

    st.markdown("---")

    # SELETOR DE TEMAS DINÂMICO
    st.subheader("✍️ Laboratório de Redação")
    try:
        themes_res = requests.get(f"{API_BASE_URL}/themes")
        if themes_res.status_code == 200:
            lista_temas = themes_res.json()
            opcoes_temas = {f"[{t['banca']}] {t['title']}": t['id'] for t in lista_temas}
            t_sel = st.selectbox("Escolha sua proposta:", list(opcoes_temas.keys()))
            THEME_ID = opcoes_temas[t_sel]
        else:
            THEME_ID = 1
    except:
        THEME_ID = 1

    essay_text = st.text_area("Seu texto:", height=350, placeholder="Inicie sua redação aqui...")
    
    if st.button("🚀 CORRIGIR AGORA", type="primary"):
        if essay_text.strip():
            with st.spinner("Nossa IA está analisando cada detalhe do seu texto..."):
                payload = {"theme_id": THEME_ID, "content": essay_text}
                res = requests.post(f"{API_BASE_URL}/essays/submit", json=payload, headers=headers)
                
                if res.status_code == 200:
                    resultado = res.json()["resultado"]
                    st.success(f"Nota Final: {resultado['final_score']}/1000")
                    
                    st.subheader("📋 Desempenho por Competência")
                    cols = st.columns(5)
                    comps = resultado["competences"]
                    for i, k in enumerate(["c1", "c2", "c3", "c4", "c5"]):
                        with cols[i]:
                            st.metric(f"Comp. {i+1}", f"{comps[k]['score']}")
                            st.caption(comps[k]['feedback'])
                    
                    st.subheader("🔍 Microaulas de Correção")
                    for idx, c in enumerate(resultado["corrections"]):
                        with st.expander(f"Erro: {c['original_text']}"):
                            st.write(f"**Sugestão:** {c['corrected_text']}")
                            st.info(f"💡 {c['micro_lesson']}")
                            
                    st.subheader("🎯 Plano de Evolução")
                    ev = resultado["evolution_plan"]
                    st.write(f"**Pontos Fortes:** {', '.join(ev['strengths'])}")
                    st.warning(f"**Próximos Passos:** {ev['next_steps']}")
                    st.info(f"📚 **Leitura:** {ev['recommended_reading']}")
                else:
                    st.error(res.json().get("detail"))