import streamlit as st
from chatbot import ChatBot
from db_handler import ChatDatabase
import datetime
from bson import ObjectId

st.set_page_config(
    page_title="🧠 Mental Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot()
if "db" not in st.session_state:
    st.session_state.db = ChatDatabase()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "delete_chat_id" not in st.session_state:
    st.session_state.delete_chat_id = None

def load_chat(chat_id):
    try:
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = st.session_state.db.get_chat_history(chat_id)
    except Exception as e:
        st.error(f"Error loading chat: {e}")
        st.session_state.current_chat_id = None
        st.session_state.messages = []

def delete_chat(chat_id):
    if st.session_state.db.delete_chat(chat_id):
        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = None
            st.session_state.messages = []
        st.success("Chat deleted successfully")
    else:
        st.error("Failed to delete chat")

# Dashboard button in the top right
col1, col2 = st.columns([5, 1])
with col2:
    if st.button("📊 Dashboard", key="dashboard_button"):
        st.switch_page("pages/dashboard.py")

# Sidebar for chat history
with st.sidebar:
    st.title("Chat History")
    
    # New chat button
    if st.button("+ New Chat"):
        new_chat_id = st.session_state.db.create_chat()
        if new_chat_id:
            load_chat(new_chat_id)
        else:
            st.error("Failed to create new chat")
    
    # List of all chats
    try:
        chats = st.session_state.db.get_all_chats()
        for chat in chats:
            chat_id = str(chat["_id"])
            created_at = chat["created_at"].strftime("%Y-%m-%d %H:%M")
            
            # Create columns for chat title and delete button
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(f"{created_at}", key=f"chat_{chat_id}"):
                    load_chat(chat_id)
            
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)
                    st.rerun()
    except Exception as e:
        st.error(f"Error loading chat history: {e}")

# Main chat area
with col1:
    st.title("Medbot : AI Mental Health Assistant")

# Chat container
chat_container = st.container()

# Display current chat
if st.session_state.current_chat_id:
    # Display all messages in the chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input area at the bottom
    user_input = st.chat_input("Type your message here...")
    if user_input:
        try:
            # Display user message immediately
            with st.chat_message("user"):
                st.write(user_input)
            
            # Get and display bot response
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.get_bot_response(
                    st.session_state.current_chat_id,
                    user_input
                )
                with st.chat_message("assistant"):
                    st.write(response)
                
                # Update session state messages
                st.session_state.messages = st.session_state.db.get_chat_history(st.session_state.current_chat_id)
                st.rerun()  # Force a rerun to update the display
        except Exception as e:
            st.error(f"Error processing message: {e}")
else:
    st.info("Select a chat from the sidebar or create a new one to start chatting.")
