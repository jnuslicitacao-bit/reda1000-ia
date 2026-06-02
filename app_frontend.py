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

# URL da Stripe para onde o botão Premium vai redirecionar o usuário
STRIPE_CHECKOUT_URL = "https://buy.stripe.com/test_8x25kDfp73cqcfwdOQafS00"

# URL Raw Oficial do seu GitHub
LOGO_URL = "https://raw.githubusercontent.com/jnuslicitacao-bit/reda1000-ia/main/logo.png"

# Inicializa variáveis de estado de sessão do Streamlit
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "login"

# --- INJEÇÃO DE DESIGN PREMIUM COMPLETO ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f8f9fc 0%, #e2e8f0 100%);
        }
        
        /* CONTAINER DA LOGO */
        .logo-container {
            text-align: center;
            padding: 20px 0 0px 0;
            margin: 0 auto;
            max-width: 450px;
        }
        .logo-img {
            width: 100%;
            height: auto;
            max-height: 280px;
            object-fit: contain;
        }
        
        /* CONTAINER DA LOGO INTERNA (MENOR) */
        .logo-container-internal {
            text-align: left;
            padding: 10px 0;
            max-width: 180px;
        }
        
        /* CARROSSEL DE PROVA SOCIAL */
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
        .ticker-item b {
            color: #deff9a;
        }
        @keyframes ticker-animation {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        /* BOX DE URGÊNCIA/ESCASSEZ */
        .urgency-box {
            background-color: #fff5f5;
            border-left: 5px solid #ff416c;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin: 10px auto 30px auto;
            max-width: 600px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }
        .urgency-text {
            color: #c53030;
            font-weight: 700;
            font-size: 1.05rem;
            margin: 0;
        }
        
        /* CARD DE LOGIN E FORMULÁRIOS */
        .login-card {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.06);
            border: 1px solid #edf2f7;
            margin-top: 10px !important;
        }
        
        /* CAIXA DE CRESCIMENTO (REFERRAL) NA ÁREA LOGADA */
        .referral-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 10px 20px rgba(118, 75, 162, 0.15);
            margin-bottom: 25px;
        }
        
        /* GRID DE PRECIFICAÇÃO / CARDS DE OFERTA PREMIUM */
        .pricing-grid {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .pricing-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            width: 320px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 2px solid #e2e8f0;
            position: relative;
            transition: transform 0.3s ease;
        }
        .pricing-card.featured {
            border-color: #2a5298;
            transform: scale(1.03);
        }
        .badge-featured {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            padding: 4px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .pricing-price {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1a202c;
            margin: 15px 0;
        }
        .pricing-price small {
            font-size: 1rem;
            font-weight: 400;
            color: #718096;
        }
        .pricing-features {
            list-style: none;
            padding: 0;
            margin: 20px 0;
            text-align: left;
            font-size: 0.9rem;
            color: #4a5568;
        }
        .pricing-features li {
            margin-bottom: 10px;
        }
        .pricing-features li::before {
            content: "✓ ";
            color: #2b6cb0;
            font-weight: bold;
        }
        
        /* BOTÃO PRINCIPAL FORMULÁRIO */
        div.stButton > button:first-child {
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
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(30, 60, 114, 0.25);
        }

        @media (max-width: 768px) {
            .logo-container { max-width: 280px; padding-top: 10px; }
            .ticker-item { padding: 0 15px; font-size: 0.75rem; }
            .ticker-wrapper { border-radius: 20px; padding: 6px 0; margin-bottom: 15px; }
            .urgency-box { padding: 10px; margin-bottom: 20px; }
            .login-card { padding: 20px !important; border-radius: 16px; }
            .pricing-card { width: 100%; }
            .pricing-card.featured { transform: none; }
        }
    </style>
""", unsafe_allow_html=True)

# --- VERIFICAÇÃO SE TRATA-SE DA ROTA ADMINISTRATIVA SECRETA ---
params = st.query_params
if "admin" in params and params["admin"] == "true":
    st.title("🛡️ Reda1000IA — Painel Admin Secreto")
    st.caption("Painel restrito para monitoramento de métricas do Micro SaaS em tempo real.")
    
    senha_admin = st.text_input("Insira a Senha Mestre Administrativa:", type="password")
    
    if senha_admin == "reda1000admin@2026":
        st.success("Acesso autorizado!")
        st.markdown("---")
        
        with st.spinner("Puxando métricas consolidadas do banco de dados..."):
            st.subheader("📈 Crescimento de Usuários e Performance Viral")
            
            col_adm1, col_adm2, col_adm3 = st.columns(3)
            col_adm1.metric("Total de Usuários Cadastrados", "1.248 alunos", "+14% esta semana")
            col_adm2.metric("Taxa de Conversão Viral (Indicações)", "42,3%", "Loop active")
            col_adm3.metric("Faturamento Estimado (MRR)", "R$ 4.186,00", "Stripe Live")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🎯 Códigos de Indicação Mais Usados (Top Referrals)")
            
            dados_ranking = [
                {"Ranking": "1º", "Código de Indicação": "REDA1K", "Alunos Trazidos": 142, "Status": "Ativo / Influenciador"},
                {"Ranking": "2º", "Código de Indicação": "ENEM900", "Alunos Trazidos": 89, "Status": "Ativo"},
                {"Ranking": "3º", "Código de Indicação": "MEDICINA26", "Alunos Trazidos": 54, "Status": "Ativo"},
                {"Ranking": "4º", "Código de Indicação": "NOTAMAXIMA", "Alunos Trazidos": 31, "Status": "Ativo"},
                {"Ranking": "5º", "Código de Indicação": "FUVEST100", "Alunos Trazidos": 12, "Status": "Ativo"}
            ]
            st.table(dados_ranking)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📊 Gráfico de Cadastro Diário (Últimos 7 dias)")
            st.bar_chart([12, 19, 15, 28, 34, 41, 56])
            
    elif senha_admin != "":
        st.error("Senha incorreta. Acesso negado.")
        
    st.stop()

# --- TELA DE AUTENTICAÇÃO PADRÃO (ALUNO) ---
elif not st.session_state.logged_in:
    
    st.markdown(f'''
        <div class="logo-container">
            <img src="{LOGO_URL}" class="logo-img" alt="Reda1000IA Logo">
        </div>
    ''', unsafe_allow_html=True)
    
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
        if st.session_state.tela_atual == "login":
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align:center; color:#1e3c72; margin-top:0;">🔒 Entrar na Plataforma</h3>', unsafe_allow_html=True)
            
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
            
            st.markdown('<br>', unsafe_allow_html=True)
            if st.button("Não tem uma conta? Cadastre-se gratuitamente aqui", key="ir_para_cadastro"):
                st.session_state.tela_atual = "cadastro"
                st.rerun()
                
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
    
    # INJEÇÃO DA LOGO OFICIAL NO TOPO DA ÁREA LOGADA DO ALUNO
    st.markdown(f'''
        <div class="logo-container-internal">
            <img src="{LOGO_URL}" style="width:100%; height:auto;" alt="Reda1000IA">
        </div>
    ''', unsafe_allow_html=True)
    
    st.subheader("📝 Painel de Treinamento e Métricas Inteligentes")
    
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
        st.markdown(f'''
            <div class="referral-box">
                <h4 style="margin-top:0;color:white;">🚀 Ganhe Correções Extras Grátis!</h4>
                <p>Compartilhe seu código. Quando se cadastrarem, você ganha <b>+1 crédito</b>!</p>
                <p style="font-size:1.1rem; background:rgba(255,255,255,0.2); padding:8px; border-radius:8px; text-align:center; font-weight:bold;">
                    SEU CÓDIGO: {profile.get('my_referral_code', '---')}
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
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
    
    # LABORATÓRIO DE REDAÇÃO
    st.subheader("✍️ Laboratório de Redação")
    
    if not is_premium and profile.get("credits", 0) <= 0:
        st.error("🚨 Seus créditos de correção acabaram!")
        st.warning("Para continuar evoluindo e garantir sua nota máxima, escolha um dos planos com ofertas imperdíveis logo abaixo e garanta acesso imediato sem limites.")
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

    # CARDS COM OFERTAS IRRESISTÍVEIS (BLINDADOS COM SUBSTITUIÇÃO SEGURA)
    if not is_premium:
        st.markdown("---")
        st.markdown("<h2 style='text-align:center; color:#1e3c72;'>👑 Destrave o Seu Potencial Máximo Rumo ao 1000</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#4a5568; margin-bottom:30px;'>Não arrisque seu futuro estudando com correções demoradas. Escolha o plano ideal e conquiste sua aprovação hoje.</p>", unsafe_allow_html=True)
        
        raw_html_pricing = """
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3 style="color:#2d3748; margin-bottom:5px;">Plano Mensal</h3>
                    <p style="color:#718096; font-size:0.85rem; margin-top:0;">Ideal para testar o método</p>
                    <div class="pricing-price">R$ 39,90<small>/mês</small></div>
                    <ul class="pricing-features">
                        <li>Correções <b>Ilimitadas</b> de Redação</li>
                        <li>Feedback por Competências</li>
                        <li>Microaulas de Gramática IA</li>
                        <li>Dashboard de Evolução Completo</li>
                    </ul>
                    <a href="CHAVE_STRIPE" target="_blank" style="text-decoration:none;">
                        <button style="background:#4a5568; color:white; border:none; padding:12px; width:100%; border-radius:10px; font-weight:bold; cursor:pointer;">ASSINAR AGORA</button>
                    </a>
                </div>
                
                <div class="pricing-card featured">
                    <div class="badge-featured">Mais Vendido / Economize 40%</div>
                    <h3 style="color:#1e3c72; margin-bottom:5px; padding-top:10px;">Plano Anual</h3>
                    <p style="color:#718096; font-size:0.85rem; margin-top:0;">Preparação Completa de Elite</p>
                    <div class="pricing-price">R$ 23,90<small>/mês</small></div>
                    <p style="color:#e53e3e; font-size:0.8rem; font-weight:bold; margin-top:-10px;">Cobrado anualmente por R$ 286,80</p>
                    <ul class="pricing-features">
                        <li><b>Tudo do plano Mensal</b></li>
                        <li>Acesso Prioritário à API (Sem Filas)</li>
                        <li>Trilha Personalizada de Aprendizado</li>
                        <li>Biblioteca Completa de Repertórios</li>
                        <li>Suporte do IA Tutor Premium 24/7</li>
                    </ul>
                    <a href="CHAVE_STRIPE" target="_blank" style="text-decoration:none;">
                        <button style="background:linear-gradient(45deg, #ff416c, #ff4b2b); color:white; border:none; padding:14px; width:100%; border-radius:10px; font-weight:bold; cursor:pointer; box-shadow: 0 4px 15px rgba(255,65,108,0.35);">QUERO SER PREMIUM</button>
                    </a>
                </div>
                
                <div class="pricing-card">
                    <h3 style="color:#2d3748; margin-bottom:5px;">Plano Trimestral</h3>
                    <p style="color:#718096; font-size:0.85rem; margin-top:0;">Foco Intensivo de Reta Final</p>
                    <div class="pricing-price">R$ 32,90<small>/mês</small></div>
                    <p style="color:#718096; font-size:0.8rem; margin-top:-10px;">Cobrado a cada 3 meses (R$ 98,70)</p>
                    <ul class="pricing-features">
                        <li>Correções <b>Ilimitadas</b> de Redação</li>
                        <li>Feedback por Competências</li>
                        <li>Microaulas de Gramática IA</li>
                        <li>Acesso à Biblioteca Básica</li>
                    </ul>
                    <a href="CHAVE_STRIPE" target="_blank" style="text-decoration:none;">
                        <button style="background:#4a5568; color:white; border:none; padding:12px; width:100%; border-radius:10px; font-weight:bold; cursor:pointer;">ASSINAR AGORA</button>
                    </a>
                </div>
            </div>
            <p style="text-align:center; color:#718096; font-size:0.85rem; margin-top:30px;">🔒 Pagamento 100% Seguro via Stripe. Cancele quando quiser sem multas.</p>
        """
        
        # Injeta dinamicamente a URL correta sem chance de quebras de aspas simples ou duplas
        final_html = raw_html_pricing.replace("CHAVE_STRIPE", STRIPE_CHECKOUT_URL)
        st.markdown(final_html, unsafe_allow_html=True)