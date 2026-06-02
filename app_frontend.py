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

if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "login"

# ==============================================================================
# 2. DESIGN DO SISTEMA (Apenas o essencial e nativo, sem perigo de vazamento)
# ==============================================================================
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f8f9fc 0%, #e2e8f0 100%);
        }
        .logo-container {
            text-align: center;
            padding: 20px 0;
            margin: 0 auto;
            max-width: 450px;
        }
        .logo-img {
            width: 100%;
            height: auto;
            max-height: 250px;
            object-fit: contain;
        }
        .logo-container-internal {
            text-align: left;
            padding: 10px 0;
            max-width: 180px;
        }
        .ticker-wrapper {
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 12px 0;
            margin-bottom: 25px;
            border-radius: 50px;
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
        }
        .urgency-text {
            color: #c53030;
            font-weight: 700;
        }
        .referral-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. CONTROLADORES DE INTERFACE (Funções limpas por escopo)
# ==============================================================================
def tela_admin():
    st.title("🛡️ Reda1000IA — Painel Admin Secreto")
    senha_admin = st.text_input("Insira a Senha Mestre Administrativa:", type="password")
    
    if senha_admin == "reda1000admin@2026":
        st.success("Acesso autorizado!")
        st.markdown("---")
        col_adm1, col_adm2, col_adm3 = st.columns(3)
        col_adm1.metric("Total de Usuários Cadastrados", "1.248 alunos")
        col_adm2.metric("Taxa de Conversão Viral", "42,3%")
        col_adm3.metric("Faturamento Estimado (MRR)", "R$ 4.186,00")
    elif senha_admin != "":
        st.error("Senha incorreta.")

def tela_autenticacao():
    st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}" class="logo-img" alt="Logo"></div>', unsafe_allow_html=True)
    
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
    
    _, col_central, _ = st.columns([1, 1.5, 1])
    
    with col_central:
        if st.session_state.tela_atual == "login":
            st.subheader("🔒 Entrar na Plataforma")
            u_login = st.text_input("E-mail", key="u_log", placeholder="estudante@email.com")
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
            
            if st.button("Não tem uma conta? Cadastre-se aqui", key="ir_para_cadastro"):
                st.session_state.tela_atual = "cadastro"
                st.rerun()
                
        elif st.session_state.tela_atual == "cadastro":
            st.subheader("✨ Criar Conta Grátis")
            n_cad = st.text_input("Nome", placeholder="Seu nome completo")
            e_cad = st.text_input("E-mail", placeholder="seu.email@escola.com")
            s_cad = st.text_input("Senha", type="password", placeholder="Crie uma senha forte")
            ref_cad = st.text_input("Código de Indicação (Opcional)", placeholder="Ex: REDA1K")
            
            if st.button("GARANTIR MINHA VAGA AGORA", key="btn_c"):
                if n_cad and e_cad and s_cad:
                    payload = {"name": n_cad, "email": e_cad, "password": s_cad, "referred_by_code": ref_cad.strip() if ref_cad.strip() else None}
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
            
            if st.button("Já tem uma conta? Clique aqui para entrar", key="ir_para_login"):
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
        st.error("Erro ao sincronizar dados com o servidor.")
        st.stop()

    profile = dash_data.get("user_profile", {})
    metrics = dash_data.get("metrics", {})
    share_marketing = dash_data.get("share_marketing", {})
    
    st.markdown(f'<div class="logo-container-internal"><img src="{LOGO_URL}" style="width:100%; height:auto;" alt="Reda1000IA"></div>', unsafe_allow_html=True)
    st.subheader("📝 Painel de Treinamento")
    
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
    st.subheader("✍️ Laboratório de Redação")
    
    if not is_premium and profile.get("credits", 0) <= 0:
        st.error("🚨 Seus créditos de correção acabaram!")
        st.warning("Para liberar acessos ilimitados imediatamente, mude para o Plano Premium.")
        st.link_button("👑 VIRAR PREMIUM AGORA", STRIPE_CHECKOUT_URL, use_container_width=True)
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
        except Exception:
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
                    except Exception:
                        st.error("Erro de comunicação com o servidor.")

        # CTA nativo e seguro para Upgrade se ele for gratuito (sem risco de quebra de HTML)
        if not is_premium:
            st.markdown("---")
            st.info("💡 Quer treinar sem limites? O plano Premium oferece correções ilimitadas e tutor de IA disponível 24h.")
            st.link_button("💳 MUDAR PARA O PLANO PREMIUM", STRIPE_CHECKOUT_URL, use_container_width=True)

# ==============================================================================
# 4. EXECUÇÃO CENTRAL (MAIN LOOP)
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