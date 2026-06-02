import streamlit as st
import requests
import datetime

# Configuração da página do Streamlit
st.set_page_config(page_title="Reda1000IA - Micro SaaS", page_icon="📝", layout="wide")

# Lógica inteligente: usa o segredo da nuvem se existir, caso contrário usa o localhost
if "API_BASE_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_BASE_URL"]
else:
    API_BASE_URL = "http://127.0.0.1:8000/api"

# Inicializa variáveis de estado de sessão do Streamlit
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- INJEÇÃO DE DESIGN PREMIUM (CSS CUSTOMIZADO) ---
st.markdown("""
    <style>
        /* Estilização do fundo e container principal */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        }
        
        /* Título principal com degradê moderno */
        .main-title {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem;
            text-align: center;
            margin-bottom: 5px;
        }
        
        /* Subtítulo atraente */
        .sub-title {
            color: #546e7a;
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 40px;
            font-weight: 400;
        }
        
        /* Customização das abas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #ffffff;
            border-radius: 12px 12px 0px 0px;
            padding: 10px 30px;
            font-weight: 600;
            color: #455a64;
            border: 1px solid #e0e0e0;
            border-bottom: none;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(45deg, #1e3c72, #2a5298) !important;
            color: white !important;
            border: none !important;
        }
        
        /* Card com bordas arredondadas e sombra suave para o formulário */
        .login-card {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border: 1px solid #e0e0e0;
            margin-top: 15px;
        }
        
        /* Inputs com cantos mais suaves */
        .stTextInput div [data-baseweb="input"] {
            border-radius: 10px !important;
        }
        
        /* Botão Primário Arredondado e com Efeito Hover */
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 12px 30px;
            font-weight: bold;
            font-size: 1rem;
            width: 100%;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 65, 108, 0.4);
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- TELA DE AUTENTICAÇÃO (LOGIN / CADASTRO) ---
if not st.session_state.logged_in:
    st.markdown('<h1 class="main-title">📝 Reda1000IA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">O seu tutor inteligente para nota máxima no ENEM e Concursos</p>', unsafe_allow_html=True)
    
    # Centralizando o formulário na tela usando colunas estruturadas
    col_espaco_esq, col_central, col_espaco_dir = st.columns([1, 1.8, 1])
    
    with col_central:
        aba_login, aba_cadastro = st.tabs(["🔒 Entrar na Conta", "✨ Criar Nova Conta"])
        
        with aba_login:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            email_login = st.text_input("E-mail", key="email_login_input", placeholder="exemplo@email.com")
            senha_login = st.text_input("Senha", type="password", key="senha_login_input", placeholder="Digite sua senha")
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            if st.button("Acessar Plataforma", type="primary", key="btn_login"):
                payload = {"username": email_login, "password": senha_login}
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", data=payload)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.logged_in = True
                        st.success("🎯 Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha incorretos. Tente novamente.")
                except Exception as e:
                    st.error(f"⚠️ Erro ao conectar ao servidor: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
                    
        with aba_cadastro:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            nome_cad = st.text_input("Nome Completo", placeholder="Seu nome completo")
            email_cad = st.text_input("E-mail de Estudante", placeholder="seu.email@escola.com")
            senha_cad = st.text_input("Escolha uma Senha", type="password", placeholder="Mínimo 6 caracteres")
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            if st.button("Cadastrar e Iniciar Gratuitamente", key="btn_cadastro"):
                if not nome_cad or not email_cad or not senha_cad:
                    st.warning("⚠️ Preencha todos os campos obrigatórios.")
                else:
                    payload = {"name": nome_cad, "email": email_cad, "password": senha_cad}
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                        if res.status_code == 201:
                            st.success("✨ Conta criada com sucesso! Mude para a aba de 'Entrar na Conta' para fazer o login.")
                        else:
                            st.error(f"❌ {res.json().get('detail', 'Erro ao cadastrar.')}")
                    except Exception as e:
                        st.error(f"⚠️ Erro de conexão: {e}")
                        
            st.markdown('</div>', unsafe_allow_html=True)

# --- ÁREA LOGADA DA PLATAFORMA ---
else:
    # Configura o cabeçalho padrão para todas as requisições autenticadas
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Busca os dados do Dashboard passando o token seguro
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard", headers=headers)
        if response.status_code == 200:
            dash_data = response.json()
        else:
            st.session_state.logged_in = False
            st.rerun()
    except:
        st.error("Erro crítico ao obter dados do painel.")
        st.stop()

    # --- TOP BAR / STATS ---
    profile = dash_data.get("user_profile", {})
    metrics = dash_data.get("metrics", {})
    
    st.title("📝 Reda1000IA — Área de Treinamento")
    
    col_user, col_xp, col_streak, col_plan, col_logout = st.columns([2, 1, 1, 2, 1])
    with col_user:
        st.metric(label="Estudante", value=profile.get("name"))
    with col_xp:
        st.metric(label="✨ Total de XP", value=f"{profile.get('xp')} XP")
    with col_streak:
        st.metric(label="🔥 Ofensiva", value=f"{profile.get('streak')} dias")
    with col_plan:
        st.metric(label="Plano Atual", value=profile.get("plan"), delta=f"{profile.get('credits')} créditos rest.")
    with col_logout:
        if st.button("Sair da Conta"):
            st.session_state.token = None
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # --- DASHBOARD INTELIGENTE ---
    st.subheader("📊 Seu Painel de Evolução")
    st.info(metrics.get("status_message"))
    
    col_avg, col_total, col_meta = st.columns(3)
    with col_avg:
        st.metric(label="Média Geral das Notas", value=metrics.get("average_score"))
    with col_total:
        st.metric(label="Redações Entregues", value=metrics.get("total_essays"))
    with col_meta:
        st.metric(label="Sua Meta", value=metrics.get("target_score"))
        
    # Gráfico de Evolução temporal
    history = dash_data.get("history", [])
    if history:
        scores = [e["score"] for e in history]
        st.line_chart(data=scores)
    else:
        st.caption("Escreva e envie seu primeiro texto para liberar o seu gráfico de evolução.")

    st.markdown("---")

    # --- SELETOR E EDITOR DE TEXTO ---
    st.subheader("✍️ Espaço de Escrita")
    
    # Busca os temas cadastrados no banco de dados dinamicamente
    try:
        themes_res = requests.get(f"{API_BASE_URL}/themes")
        if themes_res.status_code == 200:
            lista_temas = themes_res.json()
            opcoes_temas = {f"[{t['banca']}] {t['title']}": t['id'] for t in lista_temas}
            
            tema_selecionado = st.selectbox("Escolha a proposta de redação:", list(opcoes_temas.keys()))
            THEME_ID = opcoes_temas[tema_selecionado]
        else:
            THEME_ID = 1
            st.markdown("**Tema padrão:** O estigma associado às doenças mentais na sociedade brasileira")
    except:
        THEME_ID = 1
        st.markdown("**Tema padrão:** O estigma associado às doenças mentais na sociedade brasileira")

    essay_text = st.text_area(
        "Digite ou cole sua redação:",
        height=300,
        placeholder="Desenvolva sua introdução, desenvolvimento e proposta de intervenção de acordo com o tema selecionado..."
    )

    palavras = len(essay_text.split()) if essay_text else 0
    st.caption(f"Quantidade de palavras: {palavras}")

    if st.button("🚀 Enviar para Correção da IA", type="primary"):
        if not essay_text.strip():
            st.error("O campo de texto não pode estar vazio.")
        else:
            with st.spinner("Analisando gramática, competências e gerando microaulas... Aguarde."):
                payload = {
                    "theme_id": THEME_ID,
                    "content": essay_text
                }
                
                submit_res = requests.post(f"{API_BASE_URL}/essays/submit", json=payload, headers=headers)
                
                if submit_res.status_code == 200:
                    result_data = submit_res.json()
                    resultado = result_data["resultado"]
                    
                    st.success(f"🎉 Redação Avaliada! Nota Final: {resultado['final_score']}/1000")
                    
                    # Notas Detalhadas
                    st.subheader("📋 Competências Avaliadas")
                    c_cols = st.columns(5)
                    competencias = resultado["competences"]
                    for i, comp_key in enumerate(["c1", "c2", "c3", "c4", "c5"]):
                        with c_cols[i]:
                            st.metric(label=f"Comp. {i+1}", value=f"{competencias[comp_key]['score']}/200")
                            st.caption(competencias[comp_key]['feedback'])
                    
                    # Correções Gramaticais
                    st.subheader("🔍 Correções Ortográficas e Desvios")
                    corrections = resultado["corrections"]
                    if corrections:
                        for idx, corr in enumerate(corrections):
                            with st.expander(f"Desvio {idx+1}: '{corr['original_text']}' → '{corr['corrected_text']}'"):
                                st.markdown(f"**Tipo:** {corr['error_type']}")
                                st.markdown(f"**Explicação:** {corr['explanation']}")
                                st.info(f"💡 **Microaula:** {corr['micro_lesson']}")
                    else:
                        st.balloons()
                        st.success("Texto impecável! Nenhum desvio gramatical mapeado.")
                        
                    # Plano de Evolução
                    st.subheader("🎯 Plano Prático de Evolução")
                    ev_plan = resultado["evolution_plan"]
                    st.markdown("**Pontos Fortes:** " + ", ".join(ev_plan["strengths"]))
                    st.markdown("**Pontos Fracos:** " + ", ".join(ev_plan["weaknesses"]))
                    st.warning(f"**Próximos Passos:** {ev_plan['next_steps']}")
                    st.info(f"📚 **Leitura Recomendada:** {ev_plan['recommended_reading']}")
                    
                    st.button("Atualizar Dados")
                else:
                    st.error(f"Erro: {submit_res.json().get('detail')}")