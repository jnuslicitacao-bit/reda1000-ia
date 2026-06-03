import streamlit as st
import requests

# ==============================================================================
# 1. CONFIGURAÇÕES GLOBAIS E ESTADOS
# ==============================================================================
st.set_page_config(page_title="Reda1000IA - Micro SaaS", page_icon="🚀", layout="wide")

if "API_BASE_URL" in st.secrets:
    API_BASE_URL = st.secrets["API_BASE_URL"]
else:
    API_BASE_URL = "http://127.0.0.1:8000/api"

STRIPE_CHECKOUT_URL = "https://buy.stripe.com/test_8x25kDfp73cqcfwdOQafS00"
LOGO_URL = "https://raw.githubusercontent.com/jnuslicitacao-bit/reda1000-ia/main/logo.png"

# Inicialização segura dos estados de sessão do Streamlit
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "login"

# ESTADOS ADMINISTRATIVOS DE SIMULAÇÃO (Padrão: Inativo)
if "admin_simulando" not in st.session_state:
    st.session_state.admin_simulando = False
if "admin_plano_simulado" not in st.session_state:
    st.session_state.admin_plano_simulado = "FREE"

# ==============================================================================
# 2. IDENTIDADE VISUAL E DESIGN (CSS Nativo Polido)
# ==============================================================================
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f8f9fc 0%, #e2e8f0 100%);
        }
        .logo-container {
            text-align: center;
            padding: 25px 0;
            margin: 0 auto;
            max-width: 480px;
        }
        .logo-img {
            width: 100%;
            height: auto;
            max-height: 260px;
            object-fit: contain;
        }
        .ticker-wrapper {
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 12px 0;
            margin-bottom: 25px;
            border-radius: 50px;
            box-shadow: 0 4px 12px rgba(30, 60, 114, 0.15);
        }
        .ticker {
            display: flex;
            white-space: nowrap;
            animation: ticker-animation 55s linear infinite;
        }
        .ticker-item {
            color: white;
            padding: 0 45px;
            font-size: 0.95rem;
            font-weight: 500;
        }
        .ticker-item b { color: #deff9a; }
        @keyframes ticker-animation {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .urgency-box {
            background-color: #fff5f5;
            border-left: 5px solid #ff416c;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }
        .urgency-text {
            color: #c53030;
            font-weight: 700;
            font-size: 1.05rem;
        }
        .essay-laboratory-box {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 20px;
            border: 2px solid #1e3c72;
            box-shadow: 0 10px 25px rgba(30, 60, 114, 0.08);
            margin-bottom: 30px;
        }
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 14px;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(30, 60, 114, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. COMPONENTES DE INTERFACE / MÓDULOS DE TELA
# ==============================================================================
def tela_admin():
    st.title("🛡️ Reda1000IA — Painel Admin Secreto")
    senha_admin = st.text_input("Insira a Senha Mestre Administrativa:", type="password")
    
    if senha_admin == "reda1000admin@2026":
        st.success("Acesso autorizado de Administrador!")
        st.markdown("---")
        
        # --- BLOCO DE CONTROLE DE ACESSO EXCLUSIVO DO ADMIN ---
        st.subheader("👁️ Ferramenta de Simulação de Visão do Usuário")
        st.info("Ative a simulação abaixo para forçar o app a renderizar exatamente o que um tipo de aluno vê.")
        
        simular = st.toggle("Ativar Modo Simulação Visual", value=st.session_state.admin_simulando)
        st.session_state.admin_simulando = simular
        
        if simular:
            plano_escolhido = st.radio("Escolha qual Dashboard testar:", ["FREE", "PREMIUM"], index=0 if st.session_state.admin_plano_simulado == "FREE" else 1)
            st.session_state.admin_plano_simulado = plano_escolhido
            st.success(f"Modo de testes ativo! Ao fechar esta aba ou acessar o app comum, você verá a visão **{plano_escolhido}**.")
        else:
            st.warning("Simulação desativada. O app lerá o plano real do banco de dados.")
            
        st.markdown("---")
        st.subheader("📈 Métricas Macrossistêmicas Globais")
        col_adm1, col_adm2, col_adm3 = st.columns(3)
        col_adm1.metric("Total de Usuários Cadastrados", "1.248 alunos")
        col_adm2.metric("Conversão Direta Premium", "18,4%")
        col_adm3.metric("Faturamento Estimado (MRR)", "R$ 4.186,00")
    elif senha_admin != "":
        st.error("Senha incorreta.")

def tela_autenticacao():
    st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}" class="logo-img" alt="Reda1000IA"></div>', unsafe_allow_html=True)
    
    st.markdown('''
        <div class="ticker-wrapper">
            <div class="ticker">
                <div class="ticker-item">🔥 <b>Isabella G.</b> garantiu <b>940</b> na redação do ESA!</div>
                <div class="ticker-item">✨ <b>Clara Amaral.</b> nota <b>850+</b> usando a Reda1000IA</div>
                <div class="ticker-item">🎯 <b>Matheus S.</b> alcançou nota <b>980</b> no ENEM!</div>
                <div class="ticker-item">🚀 <b>Ana Clara</b> subiu de 600 para <b>920</b> em 2 semanas!</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="urgency-box"><p class="urgency-text">⚠️ RESTAM APENAS 14 VAGAS COM ACESSO GRATUITO NESTA SEMANA.</p></div>', unsafe_allow_html=True)
    
    _, col_central, _ = st.columns([1, 1.4, 1])
    
    with col_central:
        if st.session_state.tela_atual == "login":
            st.subheader("🔒 Entrar na Plataforma")
            u_login = st.text_input("E-mail", key="u_log", placeholder="seu.email@exemplo.com")
            p_login = st.text_input("Senha", type="password", key="p_log", placeholder="Digite sua senha")
            
            if st.button("ACESSAR MINHA ÁREA", type="primary", key="btn_l"):
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", data={"username": u_login, "password": p_login})
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha inválidos.")
                except Exception:
                    st.error("⚠️ Servidor offline. Tente em instantes.")
            
            if st.button("Não tem uma conta? Cadastre-se gratuitamente", key="ir_para_cadastro"):
                st.session_state.tela_atual = "cadastro"
                st.rerun()
                
        elif st.session_state.tela_atual == "cadastro":
            st.subheader("✨ Criar Conta Grátis")
            n_cad = st.text_input("Nome", placeholder="Seu nome completo")
            e_cad = st.text_input("E-mail", placeholder="seu.email@escola.com")
            s_cad = st.text_input("Senha", type="password", placeholder="Crie uma senha forte")
            
            if st.button("GARANTIR MINHA VAGA AGORA", key="btn_c"):
                if n_cad and e_cad and s_cad:
                    payload = {"name": n_cad, "email": e_cad, "password": s_cad, "referred_by_code": None}
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                        if res.status_code == 201:
                            st.success("✨ Vaga garantida! Faça seu login.")
                            st.session_state.tela_atual = "login"
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Erro no cadastro."))
                    except Exception:
                        st.error("⚠️ Erro de conexão com o servidor.")
                else:
                    st.warning("⚠️ Preencha todos os campos obrigatórios.")
            
            if st.button("Já tem uma conta? Entrar", key="ir_para_login"):
                st.session_state.tela_atual = "login"
                st.rerun()

def tela_dashboard():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard", headers=headers)
        if response.status_code == 200:
            dash_data = response.json()
        else:
            st.session_state.logged_in = False
            st.rerun()
            return
    except Exception:
        st.error("Erro crítico de sincronização com o banco de dados.")
        st.stop()

    profile = dash_data.get("user_profile", {})
    metrics = dash_data.get("metrics", {})
    
    # --- INTERVENÇÃO DA INTELIGÊNCIA ADMINISTRATIVA (OVERRIDE DE PLANO) ---
    if st.session_state.admin_simulando:
        plano_atual = st.session_state.admin_plano_simulado
        is_premium = (plano_atual == "PREMIUM")
        # Banner informativo superior avisando o admin que ele está em modo simulado
        st.warning(f"🛠️ **Modo Admin Ativo**: Você está visualizando a dashboard simulando o plano **{plano_atual}**.")
    else:
        plano_atual = profile.get("plan", "FREE")
        is_premium = (plano_atual == "PREMIUM")
        
    # LOGO CENTRALIZADA NO TOPO DO PAINEL DO ESTUDANTE
    st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}" class="logo-img" alt="Reda1000IA"></div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 2, 1])
    with c1: st.metric("Estudante", profile.get("name", "Aluno"))
    with c2: st.metric("XP Obtido", f"{profile.get('xp', 0)} XP")
    with c3: st.metric("🔥 Ofensiva", f"{profile.get('streak', 0)}d")
    
    creditos_visiveis = "Ilimitados" if is_premium else f"{profile.get('credits', 0)} rest."
    with c4: st.metric("Plano Ativo", plano_atual, creditos_visiveis)
    with c5:
        if st.button("Sair da Conta"):
            st.session_state.token = None
            st.session_state.logged_in = False
            st.session_state.admin_simulando = False # Desativa simulação ao deslogar
            st.rerun()

    st.markdown("---")
    
    # ==============================================================================
    # PAYWALL DO GRÁFICO DE DESEMPENHO (Premium Only)
    # ==============================================================================
    st.subheader("📊 Gráfico de Evolução e Desempenho")
    
    if is_premium:
        st.info(metrics.get("status_message", "Acompanhe suas notas"))
        m1, m2, m3 = st.columns(3)
        m1.metric("Média das Notas", metrics.get("average_score", 0))
        m2.metric("Redações Corrigidas", metrics.get("total_essays", 0))
        m3.metric("Meta de Corte", metrics.get("target_score", 900))
        
        history = dash_data.get("history", [])
        if history:
            st.line_chart([e["score"] for e in history])
    else:
        st.warning("🔒 Funcionalidade exclusiva do Plano Premium.")
        st.markdown(
            "> **Métricas Avançadas Ocultas:** Desbloqueie o plano Premium para gerar os gráficos automáticos de "
            "suas notas, evolução por competências do ENEM/Bancas e acompanhar sua meta histórica de aprovação."
        )

    st.markdown("---")
    
    # ==============================================================================
    # LABORATÓRIO DE REDAÇÃO DESTACADO
    # ==============================================================================
    st.markdown('<div class="essay-laboratory-box">', unsafe_allow_html=True)
    st.subheader("✍️ Laboratório de Redação")
    
    # Regra de bloqueio de escrita baseada nos créditos reais ou na simulação administrada
    if not is_premium and profile.get("credits", 0) <= 0:
        st.error("🚨 Seus créditos de correção gratuita acabaram!")
        st.info("Faça o upgrade para o Premium logo abaixo para liberar o envio e ter correções instantâneas sem limites.")
    else:
        try:
            themes_res = requests.get(f"{API_BASE_URL}/themes")
            if themes_res.status_code == 200:
                lista_temas = themes_res.json()
                opcoes_temas = {f"[{t['banca']}] {t['title']}": t['id'] for t in lista_temas}
                t_sel = st.selectbox("Selecione o tema da proposta de redação:", list(opcoes_temas.keys()))
                THEME_ID = opcoes_temas[t_sel]
            else:
                THEME_ID = 1
        except Exception:
            THEME_ID = 1

        essay_text = st.text_area("Digite ou cole seu texto completo aqui (Mínimo 7 linhas):", height=380, placeholder="Inicie sua introdução...")
        
        if st.button("🚀 ENVIAR PARA CORREÇÃO IA", type="primary"):
            if essay_text.strip():
                with st.spinner("Inteligência Artificial analisando competências..."):
                    try:
                        res = requests.post(f"{API_BASE_URL}/essays/submit", json={"theme_id": THEME_ID, "content": essay_text}, headers=headers)
                        if res.status_code == 200:
                            st.success("🎉 Redação Avaliada com sucesso! Verifique sua nota no histórico.")
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Erro ao processar envio."))
                    except Exception:
                        st.error("Erro de comunicação com o servidor de IA.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================================================
    # SEÇÃO NATIVA DE UPGRADE COM ESCASSEZ (ALTA CONVERSÃO)
    # ==============================================================================
    if not is_premium:
        st.markdown("---")
        st.markdown("<h2 style='text-align:center; color:#1e3c72; margin-bottom:0;'>👑 Seja Premium e Garanta sua Nota 900+</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#4a5568;'>Gatilho de Escassez: Restam apenas <b>7 vagas</b> com valor promocional de lote nesta hora.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        card1, card2, card3 = st.columns(3)
        
        with card1:
            st.markdown("### 🥉 Plano Mensal")
            st.markdown("## R$ 39,90 <small>/mês</small>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("* 🚀 Correções **Ilimitadas** de Redação")
            st.markdown("* 🎯 Feedback Dinâmico por Competência")
            st.markdown("* 📊 Análise Básica de Erros Gramaticais")
            st.markdown("* 🔓 Liberação do Dashboard de Treino")
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("ASSINAR PLANO MENSAL", STRIPE_CHECKOUT_URL, use_container_width=True)
            
        with card2:
            st.markdown("### 🏆 Plano Anual (Elite)")
            st.markdown("## R$ 23,90 <small>/mês</small>", unsafe_allow_html=True)
            st.markdown("<span style='color:#e53e3e; font-weight:bold;'>Economize 40% (R$ 286,80 cobrado anual)</span>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("* 🔥 **Tudo do plano Mensal**")
            st.markdown("* ⚡ **Gráfico de Evolução e Notas Liberado**")
            st.markdown("* 🚨 Suporte Prioritário na API (Sem Filas de Espera)")
            st.markdown("* 📚 Biblioteca de Repertórios Nota 1000 Completa")
            st.markdown("* 🤖 IA Tutor Premium Ativo 24h para dúvidas")
            st.link_button("⭐ QUERO O ANUAL (MAIS VENDIDO)", STRIPE_CHECKOUT_URL, use_container_width=True)
            
        with card3:
            st.markdown("### 🥈 Plano Trimestral")
            st.markdown("## R$ 32,90 <small>/mês</small>", unsafe_allow_html=True)
            st.markdown("<span style='color:#718096;'>Cobrado R$ 98,70 a cada 3 meses</span>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("* 🚀 Correções **Ilimitadas** de Redação")
            st.markdown("* 🎯 Feedback Dinâmico por Competência")
            st.markdown("* 📊 Análise Básica de Erros Gramaticais")
            st.markdown("* 🔓 Acesso à Propostas Básicas")
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("ASSINAR PLANO TRIMESTRAL", STRIPE_CHECKOUT_URL, use_container_width=True)
            
        st.caption("<p style='text-align:center; color:#718096; margin-top:20px;'>🔒 Ambiente de pagamento criptografado e assegurado pela Stripe API.</p>", unsafe_allow_html=True)

# ==============================================================================
# 4. ORQUESTRADOR DE EXECUÇÃO CENTRAL
# ==============================================================================
def main():
    if "admin" in st.query_params and st.query_params["admin"] == "true":
        tela_admin()
    elif not st.session_state.logged_in:
        tela_autenticacao()
    else:
        tela_dashboard()

if __name__ == "__main__":
    main()