'''import streamlit as st
import psycopg2
import bcrypt

# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="your_password",
        port="5432"
    )

st.title("Wellbot")

# -----------------------------
# Insert new user
# -----------------------------
def insert_user(username, password, name, age, gender, email, phone):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO accounts (username, password_hash, name, age, gender, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (username, hashed.decode('utf-8'), name, age, gender, email, phone))
    conn.commit()
    cur.close()
    conn.close()

# -----------------------------
# Verify user login
# -----------------------------
def verify_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM accounts WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        stored_hash = row[0].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False

# -----------------------------
# Reset password
# -----------------------------
def reset_password(username, new_password):
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET password_hash = %s WHERE username = %s",
                (hashed.decode('utf-8'), username))
    conn.commit()
    cur.close()
    conn.close()

# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.set_page_config(page_title="Auth System", page_icon="🔐", layout="centered")

    #  CUSTOM CSS
    st.markdown("""
        <style>
        body {
            background-color: #f4f6f9;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 1em;
        }
        .stButton button:hover {
            background-color: #45a049;
            border: 1px solid #2e7d32;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
        }
        .auth-card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Language Preference (Right Side)
    # -----------------------------
    language = st.sidebar.radio("🌐 Language", ("English", "हिन्दी"))

    texts = {
        "English": {
            "login": "Login",
            "signup": "Sign Up",
            "username": "Username",
            "password": "Password",
            "login_btn": "Login",
            "signup_btn": "Create Account",
            "welcome": "Welcome back, {user}!",
            "no_account": "Don’t have an account? Sign Up",
            "have_account": "Already have an account? Login",
            "forgot": "Forgot Password?",
            "reset": "Reset Password",
            "name": "Full Name",
            "age": "Age",
            "gender": "Gender",
            "email": "Email",
            "phone": "Phone Number"
        },
        "हिन्दी": {
            "login": "लॉगिन",
            "signup": "साइन अप",
            "username": "उपयोगकर्ता नाम",
            "password": "पासवर्ड",
            "login_btn": "लॉगिन करें",
            "signup_btn": "खाता बनाएँ",
            "welcome": "स्वागत है, {user}!",
            "no_account": "खाता नहीं है? साइन अप करें",
            "have_account": "पहले से खाता है? लॉगिन करें",
            "forgot": "पासवर्ड भूल गए?",
            "reset": "पासवर्ड रीसेट करें",
            "name": "पूरा नाम",
            "age": "आयु",
            "gender": "लिंग",
            "email": "ईमेल",
            "phone": "फ़ोन नंबर"
        }
    }
    T = texts[language]

    # -----------------------------
    # SESSION STATE
    # -----------------------------
    if "page" not in st.session_state:
        st.session_state.page = "login"

    # -----------------------------
    # LOGIN
    # -----------------------------
    if st.session_state.page == "login":
        with st.container():
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.subheader(T["login"])
            username = st.text_input(T["username"])
            password = st.text_input(T["password"], type="password")

            if st.button(T["login_btn"]):
                if verify_user(username, password):
                    st.success(T["welcome"].format(user=username))
                else:
                    st.error("❌ Invalid credentials")

            # one row for signup + forgot password
            col1, col2 = st.columns(2)
            with col1:
                if st.button(T["no_account"]):
                    st.session_state.page = "signup"
            with col2:
                if st.button(T["forgot"]):
                    st.session_state.page = "forgot"

            st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # SIGNUP
    # -----------------------------
    elif st.session_state.page == "signup":
        with st.container():
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.subheader(T["signup"])
            name = st.text_input(T["name"])
            age = st.number_input(T["age"], 0, 120, step=1)
            gender = st.selectbox(T["gender"], ["Male", "Female", "Other"] if language=="English" else ["पुरुष", "महिला", "अन्य"])
            email = st.text_input(T["email"])
            phone = st.text_input(T["phone"])
            username = st.text_input(T["username"])
            password = st.text_input(T["password"], type="password")

            if st.button(T["signup_btn"]):
                try:
                    insert_user(username, password, name, age, gender, email, phone)
                    st.success("✅ Account created! Please log in.")
                    st.session_state.page = "login"
                except Exception as e:
                    st.error(f"Error: {e}")

            if st.button(T["have_account"]):
                st.session_state.page = "login"

            st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # FORGOT PASSWORD
    # -----------------------------
    elif st.session_state.page == "forgot":
        with st.container():
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.subheader(T["reset"])
            username = st.text_input(T["username"])
            new_password = st.text_input(T["password"], type="password")

            if st.button(T["reset"]):
                try:
                    reset_password(username, new_password)
                    st.success("✅ Password reset successfully! Please login again.")
                    st.session_state.page = "login"
                except Exception as e:
                    st.error(f"Error: {e}")

            if st.button(T["have_account"]):
                st.session_state.page = "login"

            st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()'''















# app.py
import streamlit as st
from nlu import detect_intent, extract_entities
from dialog_manager import State, Context, next_step

st.set_page_config(page_title="Wellbot", page_icon="💬")
st.title("Wellbot 💬")

# If you already have login from Milestone 1, show this page after successful login.

if "state" not in st.session_state:
    st.session_state.state = State.START
if "ctx" not in st.session_state:
    st.session_state.ctx = Context()
if "history" not in st.session_state:
    st.session_state.history = []

def bot_say(text):
    st.session_state.history.append(("bot", text))

def user_say(text):
    st.session_state.history.append(("user", text))

# Initial bot prompt
if not st.session_state.history:
    bot_say("Hello! I can help with basic wellness tips. What symptom are you experiencing?")

for role, text in st.session_state.history:
    with st.chat_message("assistant" if role=="bot" else "user"):
        st.markdown(text)

user_input = st.chat_input("Type your message")
if user_input:
    user_say(user_input)
    intent = detect_intent(user_input)
    entities = extract_entities(user_input)
    reply, new_state = next_step(st.session_state.state, st.session_state.ctx, intent, entities)
    st.session_state.state = new_state
    bot_say(reply)
    st.rerun()


