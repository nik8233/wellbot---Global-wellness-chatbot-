import streamlit as st
st.title("WELLNESS BOT")
users = {
    "kani": "1234",
    "name": "number",
    "user": "bot"
}

st.title("Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in users and users[username] == password:
        st.success("Login successful")
    else:
        st.error("Invalid username or password")