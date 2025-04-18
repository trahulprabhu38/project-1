import streamlit as st
from chatbot import ChatBot
from db_handler import ChatDatabase
import datetime
from bson import ObjectId
import jwt
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize JWT secret from environment variable
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

st.set_page_config(
    page_title="🧠 Mental Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

def verify_token(token, jwt_secret=None):
    try:
        if not token:
            st.error("No token provided")
            return None
            
        # Use provided JWT secret or fall back to environment variable
        secret = jwt_secret or JWT_SECRET
            
        # Decode the token
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        
        # Get the user ID and ensure it's a string
        user_id = str(decoded.get("userId"))
        if not user_id:
            st.error("Invalid token: No user ID found")
            return None
            
        # Store the token and JWT secret in session state
        st.session_state.token = token
        if jwt_secret:
            st.session_state.jwt_secret = jwt_secret
        return user_id
        
    except jwt.exceptions.ExpiredSignatureError:
        st.error("Session expired. Please login again.")
        return None
    except jwt.exceptions.InvalidTokenError:
        st.error("Invalid session. Please login again.")
        return None
    except Exception as e:
        st.error(f"Error verifying token: {str(e)}")
        return None

# Check for authentication
token = st.query_params.get("token")
jwt_secret = st.query_params.get("jwt_secret")  # Get JWT secret from query params

if not token:
    st.error("Please login to access the chat")
    st.stop()

# Verify token and get user ID
user_id = verify_token(token, jwt_secret)
if not user_id:
    st.stop()

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
if "user_id" not in st.session_state:
    st.session_state.user_id = user_id
if "token" not in st.session_state:
    st.session_state.token = token
if "jwt_secret" not in st.session_state and jwt_secret:
    st.session_state.jwt_secret = jwt_secret

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
        new_chat_id = st.session_state.db.create_chat(user_id)
        if new_chat_id:
            load_chat(new_chat_id)
        else:
            st.error("Failed to create new chat")
    
    # List of all chats for the current user
    try:
        chats = st.session_state.db.get_all_chats(user_id)
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
