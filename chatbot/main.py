import streamlit as st
from chatbot import ChatBot
import datetime
import jwt
import requests
from dotenv import load_dotenv
import os
from encryption import encrypt_message, decrypt_message
from auth_helper import verify_and_get_user, init_auth
from recommendation_system import MoodBasedRecommender
import random
import json

load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

# API configuration
API_BASE_URL = "http://localhost:5001/api"

MOOD_WORDS = [
    "happy", "sad", "lonely", "anxious", "stressed", "angry", "depressed", 
    "worried", "upset", "excited", "tired", "overwhelmed", "nervous", 
    "exhausted", "hopeless", "shame", "fear", "panic", "self-doubt", 
    "low self-esteem", "distressed", "unmotivated", "burnt out", "guilt", 
    "grief", "emptiness", "worthless", "helpless", "restless", "isolated", 
    "insecure", "broken", "lost", "unloved", "rejected", "abandoned", 
    "confused", "betrayed", "powerless", "apathetic", "heartbroken", 
    "disconnected", "vulnerable", "regretful", "irritable", "resentful", 
    "emotional pain", "mental fatigue", "dread", "invisible", "despair", 
    "detachment", "dissociation", "emotional numbness", "self-hatred", 
    "suicidal thoughts", "desire to disappear", "feeling like a burden", 
    "thoughts of self-harm", "hopeless about future", "writing goodbye notes", 
    "emotional shutdown", "urge to escape life", "preparing for death", 
    "existential dread", "flashbacks", "social withdrawal", "mistrust", 
    "mania", "psychosis", "obsession", "compulsion", "nightmares", 
    "loss of identity", "agitation", "self-harm urges", "frustrated"
]


with open(os.path.join(os.path.dirname(__file__), 'mental_health_recommendations.json'), 'r') as f:
    LOCAL_RECOMMENDATIONS = json.load(f)

# Load mental health resources JSON
with open(os.path.join(os.path.dirname(__file__), 'mental_health_resources.json'), 'r') as f:
    MENTAL_HEALTH_RESOURCES = json.load(f)

st.set_page_config(
    page_title="🧠 Mental Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
    .chat-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-bottom: 4px;
    }
    .chat-row .chat-title-btn {
        flex: 1;
        text-align: left;
        background: none;
        border: none;
        color: inherit;
        font-size: 1em;
        cursor: pointer;
        padding: 0;
    }
    .chat-row .delete-btn {
        background: none;
        border: none;
        color: #e74c3c;
        font-size: 1.1em;
        cursor: pointer;
        margin-left: 8px;
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
        chats = st.session_state.chatbot.db.get_all_chats(st.session_state.user_id)

        if chats:
            chats = sorted(chats, key=lambda c: c.get('updated_at', c.get('created_at', '')), reverse=True)
            st.session_state.chats = chats
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
        for msg in messages:
            st.session_state.chatbot.db.add_message(
                chat_id,
                msg["role"],
                msg["content"]
            )

        load_chats()
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
        secret = jwt_secret or JWT_SECRET
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
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
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_chat_id = None
        st.session_state.chatbot = ChatBot()
        st.session_state.messages = []
        st.session_state.chats = []
        load_chats()
        if st.session_state.chats:
            st.session_state.current_chat_id = st.session_state.chats[0]["_id"]
            st.session_state.messages = load_chat_messages(st.session_state.chats[0]["_id"])

def is_mood_message(user_input):
    mood_triggers = [
        'can you recommend', 'can you suggest', 'what should i do for', 'any tips for',
        'help with', 'cope with', 'manage my', 'suggest something for', 'recommend something for'
    ]
    user_input_lower = user_input.lower()
    return any(kw in user_input_lower for kw in mood_triggers)

def get_mental_health_resources(mood=None, category=None):
    resources = []
    if mood:
        mood = mood.lower()    
    if category and category in MENTAL_HEALTH_RESOURCES:
        resources.extend(MENTAL_HEALTH_RESOURCES[category])
    else:
        resources.extend(MENTAL_HEALTH_RESOURCES.get('general', []))
    
    return resources

def format_resource_response(resources):
    if not resources:
        return "No resources found."
    
    response = "**Mental Health Resources:**\n\n"
    for i, resource in enumerate(resources, 1):
        response += f"{i}. **{resource['title']}**\n"
        if resource.get('summary'):
            response += f"   {resource['summary']}\n"
        if resource.get('url'):
            response += f"   [Read more]({resource['url']})\n"
        if resource.get('published_date'):
            response += f"   Published: {resource['published_date']}\n"
        response += "\n"
    
    return response

def process_user_input(prompt):
    if is_mood_message(prompt):
        recommendations = st.session_state.chatbot.recommender.get_recommendations(prompt)
        response = "Here are some exercises that might help you:\n\n"
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. {rec['exercise']}\n\n"
        
        resources = get_mental_health_resources()
        response += "\n" + format_resource_response(resources)
        
        response += "\nWould you like to try any of these exercises or learn more about the resources? I'm here to support you."
        return response
    return st.session_state.chatbot.get_bot_response(st.session_state.current_chat_id, prompt)

def get_latest_mood(messages):
    for msg in reversed(messages):
        if msg["role"] == "user":
            for mood in MOOD_WORDS:
                if mood in msg["content"].lower():
                    return mood
    return None

def get_external_recommendations(mood):
    url = 'https://magicloops.dev/api/loop/358a84e8-378e-47b3-9af1-9a658bbf97d4/run'
    payload = { "mood": mood }
    try:
        response = requests.get(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"youtube": [], "spotify": []}
    except Exception as e:
        print(f"API error: {e}")
        return {"youtube": [], "spotify": []}

def get_local_recommendations(mood):
    mood = mood.lower()
    recs = LOCAL_RECOMMENDATIONS.get(mood, {})
    videos = recs.get('videos', [])
    podcasts = recs.get('podcasts', [])
    return videos, podcasts

def main():
    init_auth()
    user_id = verify_and_get_user()
    if not user_id:
        return
    initialize_session_state(user_id)
    with st.sidebar:
        st.title("Chats")
        if st.button("New Chat"):
            create_chat()
        for chat in st.session_state.chats:
            chat_id = chat["_id"]
            chat_title = chat.get("title") or f"Chat {chat_id[:8]}"
            col1, col2 = st.columns([8, 1])
            with col1:
                if st.button(chat_title, key=f"select_{chat_id}"):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.messages = load_chat_messages(chat_id)
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)
                    st.rerun()
    st.title("Mental Health Assistant")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if prompt := st.chat_input("How are you feeling today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        response = process_user_input(prompt)
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state.current_chat_id:
            update_chat(st.session_state.current_chat_id, st.session_state.messages)

    mood = get_latest_mood(st.session_state.messages)
    if mood:
        if st.button("Show Recommendations"):
            exercise_recommendations = st.session_state.chatbot.recommender.get_recommendations(mood, num_recommendations=10)
            random.shuffle(exercise_recommendations)
            exercise_recommendations = exercise_recommendations[:5]
            videos, podcasts = get_local_recommendations(mood)
            response = f"Since you mentioned feeling {mood}, here are some resources that might help:\n\n"
            if exercise_recommendations:
                response += "**Recommended Exercises:**\n"
                for i, rec in enumerate(exercise_recommendations, 1):
                    response += f"{i}. {rec['exercise']}\n"
                response += "\n"
            if videos:
                response += "**Recommended YouTube Videos:**\n"
                for vid in videos:
                    response += f"- [{vid.get('title', 'Video')}]({vid.get('url', '')})\n"
            if podcasts:
                response += "\n**Recommended Spotify Podcasts:**\n"
                for pod in podcasts:
                    response += f"- [{pod.get('title', 'Podcast')}]({pod.get('url', '')})\n"
            if not exercise_recommendations and not videos and not podcasts:
                response += "Sorry, I couldn't find any recommendations for this mood."
            response += "\nWould you like to try any of these? I'm here to support you."
            with st.chat_message("assistant"):
                st.markdown(response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
            if st.session_state.current_chat_id:
                update_chat(st.session_state.current_chat_id, st.session_state.messages)

if __name__ == "__main__":
    main()
