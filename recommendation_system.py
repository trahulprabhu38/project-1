
import streamlit as st
import pandas as pd
import torch
import random
from sentence_transformers import SentenceTransformer, util

# ----------------------------
# Sample Data (Replace with your actual data source)
# ----------------------------
data = {
    "loneliness": [
        "Call a friend or family member for a quick chat.",
        "Join a community group or club that aligns with your interests."
    ],
    "anxiety": [
        "Practice deep breathing exercises for 5 minutes.",
        "Write down what’s making you anxious and challenge the thoughts."
    ],
    "depression": [
        "Go for a short walk in natural surroundings.",
        "Maintain a gratitude journal to track things you're thankful for."
    ]
}

df = pd.DataFrame([(cat, tip) for cat, tips in data.items() for tip in tips], columns=['category', 'tip'])

# ----------------------------
# WHO Mental Health API (Mocked)
# ----------------------------
def get_who_mental_health_resources():
    return [
        {"title": "WHO Mental Health Hub", "url": "https://www.who.int/teams/mental-health-and-substance-use"},
        {"title": "Crisis Helpline (WHO Directory)", "url": "https://www.who.int/mental_health/en/"},
        {"title": "Mental Health Self-Help Toolkit", "url": "https://www.who.int/publications/i/item/9789240035119"}
    ]

# ----------------------------
# Load model & encode categories
# ----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

categories = df['category'].unique().tolist()
category_embeddings = model.encode(df['category'].tolist(), convert_to_tensor=True)

# ----------------------------
# Function: get relevant tip
# ----------------------------
def get_relevant_tip(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True, device=device)
    similarity_scores = util.cos_sim(user_embedding, category_embeddings)
    best_match_idx = similarity_scores.argmax().item()
    matched_category = categories[best_match_idx]
    tips_for_category = df[df["category"] == matched_category]["tip"].tolist()
    selected_tip = random.choice(tips_for_category) if tips_for_category else "No tip available for this category."
    return matched_category, selected_tip

# ----------------------------
# Streamlit Frontend
# ----------------------------
st.title("🌱 Self-Care Recommendation System")
st.write("Tell me how you're feeling or what you're going through, and I'll suggest a self-care tip.")

user_input = st.text_input("How can I assist you with self-care today?")

if user_input:
    try:
        category, tip = get_relevant_tip(user_input)
        st.success(f"📂 **Category:** {category}\n💡 **Tip:** {tip}")
        st.markdown("### 📞 Verified Mental Health Resources (WHO):")
        for res in get_who_mental_health_resources():
            st.markdown(f"- [{res['title']}]({res['url']})")
    except Exception as e:
        st.error(f"⚠️ Oops, something went wrong: {e}")
