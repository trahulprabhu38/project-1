import streamlit as st
from chatbot import get_bot_response

st.set_page_config(page_title="🧠 Mental Health Assistant", layout="centered")
st.title("Medbot : AI Mental Health Assistant ")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def send_message():
    user_input = st.session_state.user_input
    print(user_input)
    if user_input:
        bot_response = get_bot_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_response))
        st.session_state.user_input = ""  # clear input

st.text_input("You:", key="user_input", on_change=send_message)

if st.session_state.chat_history:
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")
