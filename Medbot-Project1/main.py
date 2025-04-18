import streamlit as st
from chatbot import ChatBot
import datetime
import jwt
import requests
from dotenv import load_dotenv
import os
from encryption import encrypt_message, decrypt_message
from auth_helper import verify_and_get_user, init_auth

load_dotenv()

# Initialize JWT secret from environment variable
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

# API configuration
API_BASE_URL = "http://localhost:5001/api"

st.set_page_config(
    page_title="🧠 Mental Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        border: none;
        background-color: transparent;
        text-align: left;
        padding: 10px;
        margin: 2px 0;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: rgba(151, 166, 195, 0.15);
    }
    .chat-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: rgba(151, 166, 195, 0.1);
    }
    .assistant-message {
        background-color: transparent;
    }
    .sidebar .element-container {
        margin-bottom: 0.5rem;
    }
    div[data-testid="stSidebarNav"] {
        background-color: rgb(25, 25, 25);
    }
    section[data-testid="stSidebar"] > div {
        background-color: rgb(25, 25, 25);
    }
    .stChatMessage {
        background-color: rgba(151, 166, 195, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(method, endpoint, data=None, params=None):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            json=data,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def load_chat_messages(chat_id):
    try:
        return st.session_state.chatbot.db.get_chat_history(chat_id)
    except Exception as e:
        st.error(f"Error loading chat messages: {str(e)}")
        return []

def load_chats():
    try:
        # Get all chats for the current user
        chats = st.session_state.chatbot.db.get_all_chats(st.session_state.user_id)
        if chats:
            st.session_state.chats = chats
            
            # If no chat is selected, select the most recent one
            if not st.session_state.current_chat_id and len(chats) > 0:
                st.session_state.current_chat_id = chats[0]["_id"]
                st.session_state.messages = load_chat_messages(chats[0]["_id"])
    except Exception as e:
        st.error(f"Error loading chats: {str(e)}")

def create_chat():
    try:
        chat_id = st.session_state.chatbot.db.create_chat(st.session_state.user_id)
        if chat_id:
            load_chats()
            return chat_id
    except Exception as e:
        st.error(f"Error creating chat: {str(e)}")
    return None

def update_chat(chat_id, messages):
    try:
        # Update messages in the database
        for msg in messages:
            st.session_state.chatbot.db.add_message(
                chat_id,
                msg["role"],
                msg["content"]
            )
        return True
    except Exception as e:
        st.error(f"Error updating chat: {str(e)}")
    return False

def delete_chat(chat_id):
    try:
        if st.session_state.chatbot.db.delete_chat(chat_id):
            load_chats()
            if st.session_state.current_chat_id == chat_id:
                st.session_state.current_chat_id = None
                st.session_state.messages = []
    except Exception as e:
        st.error(f"Error deleting chat: {str(e)}")

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

def initialize_session_state(user_id):
    """Initialize all session state variables"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_chat_id = None
        st.session_state.chatbot = ChatBot()
        st.session_state.messages = []
        st.session_state.chats = []
        
        # Load chats immediately after initialization
        load_chats()
        
        # If there are chats, select the most recent one
        if st.session_state.chats:
            st.session_state.current_chat_id = st.session_state.chats[0]["_id"]
            st.session_state.messages = load_chat_messages(st.session_state.chats[0]["_id"])

# Initialize authentication
init_auth()

# Verify user and get user_id
user_id = verify_and_get_user()

# Initialize session state with all required variables
initialize_session_state(user_id)

# Add navigation to dashboard
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/dashboard.py")

# Sidebar for chat history
with st.sidebar:
    st.title("Chat History")
    
    # New chat button
    if st.button("+ New Chat", key="new_chat"):
        new_chat_id = create_chat()
        if new_chat_id:
            st.session_state.current_chat_id = new_chat_id
            st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    
    # List of chats
    if st.session_state.chats:
        for chat in st.session_state.chats:
            chat_id = chat["_id"]
            col1, col2 = st.columns([4, 1])
            with col1:
                # Get chat title
                chat_title = chat.get("title", "New Chat")
                
                # Create a button with the chat title
                button_style = "background-color: rgba(151, 166, 195, 0.15);" if chat_id == st.session_state.current_chat_id else ""
                if st.button(f"💬 {chat_title}", key=f"chat_{chat_id}"):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.messages = load_chat_messages(chat_id)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)
                    st.rerun()
    else:
        st.info("No chats yet. Start a new chat!")

# Main chat area
st.title("Medbot : AI Mental Health Assistant")

# Chat container
chat_container = st.container()

# Display current chat
with chat_container:
    if st.session_state.current_chat_id:
        # Display all messages in the chat
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input area at the bottom
        user_input = st.chat_input("Type your message here...")
        if user_input:
            try:
                # Save user message to database and update state
                st.session_state.chatbot.db.add_message(
                    st.session_state.current_chat_id,
                    "user",
                    user_input
                )
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Display user message
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                # Get and display bot response
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.get_bot_response(
                        st.session_state.current_chat_id,
                        user_input
                    )
                    
                    # Save bot response to database and update state
                    st.session_state.chatbot.db.add_message(
                        st.session_state.current_chat_id,
                        "assistant",
                        response
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Display bot response
                    with st.chat_message("assistant"):
                        st.markdown(response)
                
                # Reload chats to update titles
                load_chats()
                st.rerun()
                
            except Exception as e:
                st.error(f"Error processing message: {e}")
    else:
        st.info("Select a chat from the sidebar or create a new one to start chatting.")

# Load chats on initial render
if not st.session_state.chats:
    load_chats()
