import streamlit as st
import requests
import streamlit.components.v1 as components

# ==============================================================================
# CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Reda1000IA",
    page_icon="🚀",
    layout="wide"
)

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://127.0.0.1:8000/api")
STRIPE_CHECKOUT_URL = "https://buy.stripe.com/test_8x25kDfp73cqcfwdOQafS00"
LOGO_URL = "https://raw.githubusercontent.com/jnuslicitacao-bit/reda1000-ia/main/logo.png"

# STATES
if "token" not in st.session_state:
    st.session_state.token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ==============================================================================
# CSS PREMIUM
# ==============================================================================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #f4f7fb, #e6ecf5);
}

/* LOGO CENTRALIZADO */
.logo-center {
    display:flex;
    justify-content:center;
    margin-top:20px;
    margin-bottom:20px;
}

/* CARD LOGIN */
.login-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.08);
}

/* CAIXA REDAÇÃO (DESTAQUE PRINCIPAL) */
.text-area-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
}

.text-area-box:hover {
    border: 2px solid #2a5298;
    box-shadow: 0 0 25px rgba(42,82,152,0.2);
}

/* TEXTAREA */
textarea {
    border-radius: 12px !important;
    border: 1px solid #cbd5e0 !important;
    padding: 15px !important;
}

/* BOTÃO PRINCIPAL */
div.stButton > button:first-child {
    background: linear-gradient(45deg, #1e3c72, #2a5298);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 14px;
    font-weight: bold;
    width: 100%;
}

/* TÍTULO */
.main-title {
    text-align:center;
    color:#1e3c72;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# PRICING
# ==============================================================================
def render_pricing():
    html = f"""
    <div style="display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">

        <div style="background:white;padding:25px;border-radius:15px;width:300px;text-align:center;">
            <h3>Plano Mensal</h3>
            <h2>R$ 39,90</h2>
            <p>/mês</p>
            <a href="{STRIPE_CHECKOUT_URL}" target="_blank">
                <button style="width:100%;padding:10px;background:#1e3c72;color:white;border:none;border-radius:10px;">
                    Assinar
                </button>
            </a>
        </div>

        <div style="background:white;padding:25px;border-radius:15px;width:300px;text-align:center;border:2px solid #ff416c;">
            <h3>🔥 Plano Anual</h3>
            <h2>R$ 23,90</h2>
            <p>/mês</p>
            <p><b>Mais vendido</b></p>
            <a href="{STRIPE_CHECKOUT_URL}" target="_blank">
                <button style="width:100%;padding:12px;background:#ff416c;color:white;border:none;border-radius:10px;">
                    Ser Premium
                </button>
            </a>
        </div>

    </div>
    """
    components.html(html, height=400)

# ==============================================================================
# AUTH
# ==============================================================================
def auth_screen():
    st.markdown(f'<div class="logo-center"><img src="{LOGO_URL}" width="260"></div>', unsafe_allow_html=True)

    col = st.columns([1,2,1])[1]

    with col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        if st.session_state.page == "login":
            st.subheader("Entrar")

            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.button("Acessar"):
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/auth/login",
                        data={"username": email, "password": senha}
                    )

                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Login inválido")
                except:
                    st.error("Servidor offline")

            if st.button("Criar conta"):
                st.session_state.page = "register"
                st.rerun()

        else:
            st.subheader("Cadastro")

            nome = st.text_input("Nome")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.button("Cadastrar"):
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/auth/register",
                        json={
                            "name": nome,
                            "email": email,
                            "password": senha
                        }
                    )

                    if res.status_code == 201:
                        st.success("Conta criada!")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar")
                except:
                    st.error("Erro servidor")

            if st.button("Voltar login"):
                st.session_state.page = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# DASHBOARD
# ==============================================================================
def dashboard():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    try:
        res = requests.get(f"{API_BASE_URL}/dashboard", headers=headers)

        if res.status_code != 200:
            st.session_state.logged_in = False
            st.rerun()

        data = res.json()

    except:
        st.error("Erro servidor")
        return

    user = data.get("user_profile", {})

    # LOGO CENTRAL
    st.markdown(f'<div class="logo-center"><img src="{LOGO_URL}" width="180"></div>', unsafe_allow_html=True)

    st.markdown('<h2 class="main-title">📊 Seu Painel de Evolução</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("XP", user.get("xp", 0))
    col2.metric("🔥 Streak", user.get("streak", 0))
    col3.metric("Plano", user.get("plan", "FREE"))

    st.markdown("---")

    st.subheader("✍️ Escreva sua Redação")

    # CAIXA DESTACADA
    st.markdown('<div class="text-area-box">', unsafe_allow_html=True)

    texto = st.text_area("Digite sua redação abaixo:", height=300)

    if st.button("🚀 Corrigir Redação"):
        if texto.strip():
            with st.spinner("Corrigindo com IA..."):
                try:
                    r = requests.post(
                        f"{API_BASE_URL}/essays/submit",
                        json={"content": texto},
                        headers=headers
                    )

                    if r.status_code == 200:
                        st.success("✅ Redação corrigida com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao corrigir")
                except:
                    st.error("Erro servidor")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if user.get("plan") != "PREMIUM":
        st.markdown("## 🔓 Desbloqueie o Premium")
        render_pricing()

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if not st.session_state.logged_in:
        auth_screen()
    else:
        dashboard()

if __name__ == "__main__":
    main()