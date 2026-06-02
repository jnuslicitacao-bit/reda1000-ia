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

# Inicializa variáveis de estado de sessão
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- INJEÇÃO DE DESIGN PREMIUM COM PROVA SOCIAL E ESCASSEZ ---
st.markdown("""
    <style>
        /* Estilização do fundo */
        .stApp {
            background: linear-gradient(135deg, #f8f9fc 0%, #e2e8f0 100%);
        }
        
        /* Container da LOGO */
        .logo-container {
            text-align: center;
            padding-top: 20px;
            margin-bottom: 0px;
        }
        .logo-text {
            font-family: 'Trebuchet MS', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            letter-spacing: -2px;
            margin: 0;
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .logo-dot {
            color: #ff416c;
            -webkit-text-fill-color: #ff416c;
        }
        
        /* Frase de Escassez e Urgência */
        .urgency-box {
            background-color: #fff5f5;
            border-left: 5px solid #ff416c;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin: 20px auto 40px auto;
            max-width: 600px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .urgency-text {
            color: #c53030;
            font-weight: 700;
            font-size: 1.1rem;
            margin: 0;
        }
        
        /* Ticker de Prova Social (Alunos alcançando notas) */
        .ticker-wrapper {
            width: 100%;
            overflow: hidden;
            background: #1e3c72;
            padding: 10px 0;
            margin-bottom: 30px;
            border-radius: 50px;
        }
        .ticker {
            display: flex;
            white-space: nowrap;
            animation: ticker-animation 30s linear infinite;
        }
        .ticker-item {
            color: white;
            padding: 0 40px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .ticker-item b {
            color: #deff9a; /* Cor de destaque para a nota */
        }
        @keyframes ticker-animation {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        /* Card de Autenticação */
        .login-card {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            border: 1px solid #edf2f7;
        }
        
        /* Botão Customizado */
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 15px;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 20px rgba(30, 60, 114, 0.2);
        }
    </style>
""", unsafe_allow_html=True)


# --- TELA DE AUTENTICAÇÃO ---
if not st.session_state.logged_in:
    
    # 1. LOGO PROFISSIONAL
    st.markdown('''
        <div class="logo-container">
            <h1 class="logo-text">Reda1000<span class="logo-dot">IA</span></h1>
        </div>
    ''', unsafe_allow_html=True)
    
    # 2. PROVA SOCIAL (TICKER ANIMADO)
    st.markdown('''
        <div class="ticker-wrapper">
            <div class="ticker">
                <div class="ticker-item">🎯 <b>Matheus S.</b> alcançou nota <b>980</b> no ENEM!</div>
                <div class="ticker-item">🚀 <b>Ana Clara</b> subiu de 600 para <b>920</b> em 2 semanas!</div>
                <div class="ticker-item">🔥 <b>João Pedro</b> garantiu <b>940</b> na redação do TJ-SP!</div>
                <div class="ticker-item">✨ <b>Carla M.</b> nota <b>900+</b> usando a Reda1000IA</div>
                <div class="ticker-item">🎯 <b>Lucas F.</b> nota <b>960</b> com nosso método!</div>
                <div class="ticker-item">🚀 <b>Beatriz H.</b> nota <b>940</b> na Fuvest!</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # 3. FRASE DE ESCASSEZ E URGÊNCIA
    st.markdown('''
        <div class="urgency-box">
            <p class="urgency-text">
                ⚠️ RESTAM APENAS <b>14 VAGAS</b> COM ACESSO GRATUITO NESTA SEMANA.<br>
                <small>A oferta de lançamento encerra hoje às 23:59.</small>
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Centralização do Formulário
    _, col_central, _ = st.columns([1, 1.6, 1])
    
    with col_central:
        tab_login, tab_cad = st.tabs(["🔒 Entrar", "✨ Criar Conta Grátis"])
        
        with tab_login:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            u_login = st.text_input("E-mail", key="u_log", placeholder="estudante@email.com")
            p_login = st.text_input("Senha", type="password", key="p_log")
            
            if st.button("ACESSAR MINHA ÁREA", type="primary", key="btn_l"):
                payload = {"username": u_login, "password": p_login}
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", data=payload)
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("E-mail ou senha inválidos.")
                except:
                    st.error("Servidor offline. Tente em instantes.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab_cad:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            n_cad = st.text_input("Nome")
            e_cad = st.text_input("E-mail")
            s_cad = st.text_input("Senha", type="password")
            
            if st.button("GARANTIR MINHA VAGA AGORA", key="btn_c"):
                if n_cad and e_cad and s_cad:
                    payload = {"name": n_cad, "email": e_cad, "password": s_cad}
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                        if res.status_code == 201:
                            st.success("Conta criada! Volte para a aba 'Entrar'.")
                        else:
                            st.error(res.json().get("detail", "Erro no cadastro."))
                    except:
                        st.error("Erro de conexão.")
                else:
                    st.warning("Preencha todos os campos.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- ÁREA LOGADA ---
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Recuperação de dados do Dashboard
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