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
# CSS
# ==============================================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8f9fc, #e2e8f0);
}

.login-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.pricing-title {
    text-align:center;
    color:#1e3c72;
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# HTML PRICING (AGORA FUNCIONANDO 100%)
# ==============================================================================
def render_pricing():
    html = f"""
    <div style="display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">

        <div style="background:white;padding:25px;border-radius:15px;width:300px;text-align:center;">
            <h3>Plano Mensal</h3>
            <h2>R$ 39,90</h2>
            <p>/mês</p>
            <ul style="text-align:left;">
                <li>Correções ilimitadas</li>
                <li>Dashboard completo</li>
            </ul>
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
# LOGIN / CADASTRO
# ==============================================================================
def auth_screen():
    st.image(LOGO_URL, width=250)

    col = st.columns([1,2,1])[1]

    with col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        if st.session_state.page == "login":
            st.subheader("Login")

            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.button("Entrar"):
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
    metrics = data.get("metrics", {})

    st.image(LOGO_URL, width=150)

    st.title("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("XP", user.get("xp", 0))
    col2.metric("Streak", user.get("streak", 0))
    col3.metric("Plano", user.get("plan", "FREE"))

    st.markdown("---")

    st.subheader("Nova Redação")

    texto = st.text_area("Digite sua redação", height=250)

    if st.button("Corrigir"):
        if texto.strip():
            with st.spinner("Corrigindo..."):
                try:
                    r = requests.post(
                        f"{API_BASE_URL}/essays/submit",
                        json={"content": texto},
                        headers=headers
                    )

                    if r.status_code == 200:
                        st.success("Corrigido!")
                        st.rerun()
                    else:
                        st.error("Erro")
                except:
                    st.error("Servidor erro")

    st.markdown("---")

    if user.get("plan") != "PREMIUM":
        st.markdown("## 🔓 Desbloquear Premium")
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