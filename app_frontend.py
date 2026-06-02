import streamlit as st
import requests
import streamlit.components.v1 as components

# ==============================================================================
# CONFIG
# ==============================================================================
st.set_page_config(page_title="Reda1000IA", page_icon="🚀", layout="wide")

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
# CSS NOVO (UI PROFISSIONAL)
# ==============================================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e3c72);
}

/* LOGO CENTRAL */
.logo-center {
    text-align:center;
    margin-top:20px;
}
.logo-center img {
    max-width:280px;
}

/* CARD */
.card {
    background: white;
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

/* TEXTAREA DESTACADA */
textarea {
    border-radius: 15px !important;
    border: 2px solid #1e3c72 !important;
    padding: 15px !important;
    font-size: 16px !important;
    box-shadow: 0 0 15px rgba(30,60,114,0.2);
}

textarea:focus {
    border: 2px solid #ff416c !important;
    box-shadow: 0 0 20px rgba(255,65,108,0.6);
}

/* BOTÕES */
.stButton>button {
    border-radius: 12px;
    font-weight: bold;
    padding: 12px;
}

/* PREMIUM BUTTON */
.btn-premium {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    padding: 12px;
    border-radius: 10px;
    border:none;
    width:100%;
    font-weight:bold;
}

/* FREE BUTTON */
.btn-free {
    background: #334155;
    color: white;
    padding: 12px;
    border-radius: 10px;
    border:none;
    width:100%;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# PRICING MODERNO
# ==============================================================================
def render_pricing():
    html = f"""
    <div style="display:flex; gap:20px; justify-content:center; margin-top:20px;">

        <div style="background:white;padding:25px;border-radius:15px;width:280px;text-align:center;">
            <h3>Plano FREE</h3>
            <h2>Grátis</h2>
            <p>3 correções</p>

            <button class="btn-free">USAR GRÁTIS</button>
        </div>

        <div style="background:white;padding:25px;border-radius:15px;width:280px;text-align:center;border:3px solid #ff416c;">
            <h3>🔥 PREMIUM</h3>
            <h2>R$ 23,90</h2>
            <p>/mês</p>

            <a href="{STRIPE_CHECKOUT_URL}" target="_blank">
                <button class="btn-premium">QUERO SER PREMIUM</button>
            </a>
        </div>

    </div>
    """
    components.html(html, height=300)

# ==============================================================================
# LOGIN
# ==============================================================================
def auth_screen():
    st.markdown(f'<div class="logo-center"><img src="{LOGO_URL}"></div>', unsafe_allow_html=True)

    col = st.columns([1,2,1])[1]

    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if st.session_state.page == "login":
            st.subheader("🔒 Entrar")

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
            st.subheader("✨ Criar conta")

            nome = st.text_input("Nome")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.button("Cadastrar"):
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/auth/register",
                        json={"name": nome, "email": email, "password": senha}
                    )

                    if res.status_code == 201:
                        st.success("Conta criada!")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Erro cadastro")
                except:
                    st.error("Erro servidor")

            if st.button("Voltar"):
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
        data = res.json()
    except:
        st.error("Erro servidor")
        return

    user = data.get("user_profile", {})

    # LOGO CENTRAL
    st.markdown(f'<div class="logo-center"><img src="{LOGO_URL}"></div>', unsafe_allow_html=True)

    st.title("🚀 Painel Inteligente")

    col1, col2, col3 = st.columns(3)
    col1.metric("XP", user.get("xp", 0))
    col2.metric("Streak", user.get("streak", 0))
    col3.metric("Plano", user.get("plan", "FREE"))

    st.markdown("---")

    st.subheader("✍️ Escreva sua redação")

    texto = st.text_area(
        "Digite sua redação abaixo",
        height=300,
        placeholder="Comece sua redação aqui..."
    )

    if st.button("🚀 CORRIGIR AGORA"):
        if texto.strip():
            with st.spinner("Analisando com IA..."):
                try:
                    r = requests.post(
                        f"{API_BASE_URL}/essays/submit",
                        json={"content": texto},
                        headers=headers
                    )

                    if r.status_code == 200:
                        st.success("Redação corrigida!")
                        st.rerun()
                    else:
                        st.error("Erro")
                except:
                    st.error("Servidor erro")

    st.markdown("---")

    if user.get("plan") != "PREMIUM":
        st.subheader("🔓 Liberar acesso completo")
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