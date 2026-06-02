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

# URL de entrega direta da imagem hospedada no seu repositório principal
LOGO_URL = "https://raw.githubusercontent.com/jnuslicitacao-bit/reda1000-ia/main/logo.png" 

# Inicializa variáveis de estado de sessão do Streamlit
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "login"

# --- INJEÇÃO DE DESIGN PREMIUM COMPLETO ---
st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, #f8f9fc 0%, #e2e8f0 100%);
        }}
        
        /* CONTAINER DA LOGO */
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
        
        /* CARROSSEL DE PROVA SOCIAL */
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
        
        /* CARD DE LOGIN E FORMULÁRIOS */
        .login-card {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.06);
            border: 1px solid #edf2f7;
            margin-top: 10px !important;
        }}
        
        /* CAIXA DE CRESCIMENTO (REFERRAL) NA ÁREA LOGADA */
        .referral-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 10px 20px rgba(118, 75, 162, 0.15);
            margin-bottom: 25px;
        }}
        
        /* BOTÃO PRINCIPAL FORMULÁRIO */
        div.stButton > button:first-child {{
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 14px;
            font-weight: bold;
            width: 100%;
            margin: 20px auto 0 auto;
            display: block;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }}
        div.stButton > button:first-child:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(30, 60, 114, 0.25);
        }}

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
    
    # 1. LOGO EM IMAGEM
    st.markdown(f'''
        <div class="logo-container">
            <img src="{LOGO_URL}" class="logo-img" alt="Reda1000IA Logo">
        </div>
    ''', unsafe_allow_html=True)
    
    # 2. CARROSSEL DE PROVA SOCIAL
    st.markdown('''
        <div class="ticker-wrapper">
            <div class="ticker">
                <div class="ticker-item">🔥 <b>Isabella G.</b> garantiu <b>940</b> na redação do ESA!</div>
                <div class="ticker-item">✨ <b>Clara Amaral.</b> nota <b>850+</b> usando a Reda1000IA</div>
                <div class="ticker-item">🎯 <b>Matheus S.</b> alcançou nota <b>980</b> no ENEM!</div>
                <div class="ticker-item">🚀 <b>Ana Clara</b> subiu de 600 para <b>920</b> em 2 semanas!</div>
                <div class="ticker-item">🔥 <b>João Pedro</b> garantiu <b>940</b> na redação do TJ-SP!</div>
                <div class="ticker-item">✨ <b>Carla M.</b> nota <b>900+</b> usando a Reda1000IA</div>
                <div class="ticker-item">🎯 <b>Lucas F.</b> nota <b>960</b> com nosso método!</div>
                <div class="ticker-item">🚀 <b>Beatriz G.</b> nota <b>940</b> na Fuvest!</div>
                <div class="ticker-item">🚀 <b>Carolina F.</b> subiu de 410 para <b>880</b> em 3 semanas!</div>
                
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # 3. BOX DE URGÊNCIA
    st.markdown('''
        <div class="urgency-box">
            <p class="urgency-text">
                ⚠️ RESTAM APENAS <b>14 VAGAS</b> COM ACESSO GRATUITO NESTA SEMANA.<br>
                <small>A oferta de lançamento encerra hoje às 23:59.</small>
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    _, col_central, _ = st.columns([1, 1.6, 1])
    
    with col_central:
        # --- SUB-TELA DE LOGIN ---
        if st.session_state.tela_atual == "login":
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align:center; color:#1e3c72; margin-top:0;">🔒 Entrar na Plataforma</h3>', unsafe_allow_html=True)
            
            u_login = st.text_input("E-mail", key="u_log", placeholder="estudante@email.com")
            p_login = st.text_input("Senha", type="password", key="p_log", placeholder="Digite sua senha")
            
            if st.button("ACESSAR MINHA ÁREA", type="primary", key="btn_l"):
                # Correção: O OAuth2PasswordRequestForm espera dados via parâmetro data (Form-data)
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
            
            st.markdown('<br>', unsafe_allow_html=True)
            if st.button("Não tem uma conta? Cadastre-se gratuitamente aqui", key="ir_para_cadastro"):
                st.session_state.tela_atual = "cadastro"
                st.rerun()
                
        # --- SUB-TELA DE CADASTRO ---
        elif st.session_state.tela_atual == "cadastro":
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align:center; color:#1e3c72; margin-top:0;">✨ Criar Conta Grátis</h3>', unsafe_allow_html=True)
            
            n_cad = st.text_input("Nome", placeholder="Seu nome completo")
            e_cad = st.text_input("E-mail", placeholder="seu.email@escola.com")
            s_cad = st.text_input("Senha", type="password", placeholder="Crie uma senha forte")
            ref_cad = st.text_input("Código de Indicação (Opcional)", placeholder="Ex: REDA1K")
            
            if st.button("GARANTIR MINHA VAGA AGORA", key="btn_c"):
                if n_cad and e_cad and s_cad:
                    payload = {
                        "name": n_cad, 
                        "email": e_cad, 
                        "password": s_cad,
                        "referred_by_code": ref_cad.strip() if ref_cad.strip() else None
                    }
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                        if res.status_code == 201:
                            st.success("✨ Vaga garantida com sucesso! Faça o login usando seus dados.")
                            st.session_state.tela_atual = "login"
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Erro no cadastro."))
                    except:
                        st.error("⚠️ Erro de conexão.")
                else:
                    st.warning("⚠️ Preencha todos os campos obrigatórios.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<br>', unsafe_allow_html=True)
            if st.button("Já tem uma conta? Clique aqui para entrar", key="ir_para_login"):
                st.session_state.tela_atual = "login"
                st.rerun()

# --- ÁREA LOGADA DA PLATAFORMA ---
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
        st.error("Erro crítico ao obter dados da API. Tente novamente.")
        st.stop()

    profile = dash_data.get("user_profile", {})
    metrics = dash_data.get("metrics", {})
    share_marketing = dash_data.get("share_marketing", {})
    
    st.title("📝 Reda1000IA — Painel de Treinamento")
    
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 2, 1])
    with c1: st.metric("Estudante", profile.get("name", "Aluno"))
    with c2: st.metric("XP Obtido", f"{profile.get('xp', 0)} XP")
    with c3: st.metric("🔥 Ofensiva", f"{profile.get('streak', 0)}d")
    
    is_premium = profile.get("plan") == "PREMIUM"
    creditos_visiveis = "Ilimitados" if is_premium else f"{profile.get('credits', 0)} rest."
    with c4: st.metric("Plano Ativo", profile.get("plan", "FREE"), creditos_visiveis)
    with c5:
        if st.button("Sair da Conta"):
            st.session_state.token = None
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")
    
    col_share_esq, col_share_dir = st.columns(2)
    with col_share_esq:
        st.markdown(f"""
            <div class="referral-box">
                <h4 style="margin-top:0;color:white;">🚀 Ganhe Correções Extras Grátis!</h4>
                <p>Compartilhe seu código. Quando se cadastrarem, você ganha <b>+1 crédito</b>!</p>
                <p style="font-size:1.1rem; background:rgba(255,255,255,0.2); padding:8px; border-radius:8px; text-align:center; font-weight:bold;">
                    SEU CÓDIGO: {profile.get('my_referral_code', '---')}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_share_dir:
        st.subheader("📢 Compartilhar sua Evolução")
        st.code(share_marketing.get("copy_text", "Treinando redação na Reda1000IA!"), language="text")
        if st.button("Copiar Texto de Sucesso"):
            st.toast("Texto copiado!", icon="📋")

    st.markdown("---")
    st.subheader("📊 Gráfico de Desempenho")
    st.info(metrics.get("status_message", "Acompanhe suas notas"))
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Média das Notas", metrics.get("average_score", 0))
    m2.metric("Redações Corrigidas", metrics.get("total_essays", 0))
    m3.metric("Meta de Corte", metrics.get("target_score", 900))
        
    history = dash_data.get("history", [])
    if history:
        st.line_chart([e["score"] for e in history])

    st.markdown("---")
    st.subheader("✍️ Laboratório de Redação")
    
    if not is_premium and profile.get("credits", 0) <= 0:
        st.error("🚨 Seus créditos de correção acabaram!")
        st.warning("Indique amigos para ganhar mais ou faça upgrade para o Premium.")
    else:
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

        essay_text = st.text_area("Seu texto:", height=350, placeholder="Escreva sua redação aqui...")
        
        if st.button("🚀 CORRIGIR AGORA", type="primary"):
            if essay_text.strip():
                with st.spinner("Analisando seu texto..."):
                    try:
                        res = requests.post(f"{API_BASE_URL}/essays/submit", json={"theme_id": THEME_ID, "content": essay_text}, headers=headers)
                        if res.status_code == 200:
                            st.success("🎉 Redação Avaliada com sucesso!")
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Erro ao processar."))
                    except:
                        st.error("Erro de comunicação com o servidor.")