import streamlit as st
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

def init_auth():
    """Initialize authentication state"""
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "token" not in st.session_state:
        st.session_state.token = None

def verify_and_get_user():
    """Verify token and return user_id"""
    init_auth()
    
    # If already authenticated in session, return user_id
    if st.session_state.is_authenticated and st.session_state.user_id:
        return st.session_state.user_id
    
    # Try to get token from query params
    token = st.query_params.get("token")
    
    if not token:
        st.error("Please login to access this page")
        st.stop()
    
    try:
        # Decode the token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = str(decoded.get("userId"))
        
        if not user_id:
            st.error("Invalid token: No user ID found")
            st.stop()
        
        # Store in session state
        st.session_state.is_authenticated = True
        st.session_state.user_id = user_id
        st.session_state.token = token
        
        return user_id
        
    except jwt.exceptions.ExpiredSignatureError:
        st.error("Session expired. Please login again.")
        st.session_state.is_authenticated = False
        st.stop()
    except jwt.exceptions.InvalidTokenError:
        st.error("Invalid session. Please login again.")
        st.session_state.is_authenticated = False
        st.stop()
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.session_state.is_authenticated = False
        st.stop()

def get_current_user():
    """Get current authenticated user ID"""
    if not st.session_state.is_authenticated:
        return None
    return st.session_state.user_id

def logout():
    """Clear authentication state"""
    st.session_state.is_authenticated = False
    st.session_state.user_id = None
    st.session_state.token = None 