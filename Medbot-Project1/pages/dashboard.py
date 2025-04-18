import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from db_handler import ChatDatabase
from encryption import decrypt_message
from auth_helper import verify_and_get_user

# Initialize database
db = ChatDatabase()

def get_chat_data(user_id):
    """Get chat data for the specified user"""
    # Get chats for the current user
    chats = list(db.chats.find({"user_id": user_id}))
    data = []
    
    for chat in chats:
        try:
            chat_id = str(chat["_id"])
            created_at = chat.get("created_at", datetime.now())  # Default if missing
            messages = chat.get("messages", [])
            
            # Calculate chat statistics
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            bot_messages = [msg for msg in messages if msg.get("role") == "assistant"]
            
            # Get the first user message as title
            first_user_msg = next((msg for msg in messages if msg.get("role") == "user"), None)
            title = "New Chat"
            if first_user_msg:
                try:
                    content = decrypt_message(first_user_msg.get("content", ""))
                    title = content[:40] + "..." if len(content) > 40 else content
                except:
                    pass
            
            data.append({
                "chat_id": chat_id,
                "title": title,
                "created_at": created_at,
                "total_messages": len(messages),
                "user_messages": len(user_messages),
                "bot_messages": len(bot_messages)
            })
        except Exception as e:
            print(f"Error processing chat {chat.get('_id')}: {e}")
            continue
            
    return pd.DataFrame(data)

def main():
    st.set_page_config(layout="wide")
    st.title("📊 Chat Analytics Dashboard")
    
    # Verify user and get user_id using the auth helper
    user_id = verify_and_get_user()
    
    # Add a back to chat button
    if st.button("← Back to Chat"):
        st.switch_page("main.py")
    
    # Get data for the current user
    chat_data = get_chat_data(user_id)
    
    if len(chat_data) == 0:
        st.info("No chat data available yet. Start chatting to see analytics!")
        return
    
    # Convert datetime to date for filtering
    chat_data['date'] = pd.to_datetime(chat_data['created_at']).dt.date
    
    # Get min and max dates
    min_date = chat_data['date'].min()
    max_date = chat_data['date'].max()
    
    # Sidebar filters
    st.sidebar.title("Filters")
    
    # Date range with safe defaults
    default_start = max(min_date, max_date - timedelta(days=7))
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(default_start, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    if len(date_range) == 2:
        mask = (chat_data['date'] >= date_range[0]) & (chat_data['date'] <= date_range[1])
        filtered_data = chat_data[mask]
    else:
        filtered_data = chat_data
    
    # KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Chats", len(filtered_data))
    with col2:
        st.metric("Total Messages", filtered_data["total_messages"].sum())
    with col3:
        avg_messages = filtered_data["total_messages"].mean()
        st.metric("Avg Messages per Chat", round(avg_messages, 1) if pd.notnull(avg_messages) else 0)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Message Distribution
        message_data = pd.DataFrame({
            'type': ['User Messages', 'Bot Messages'],
            'count': [
                filtered_data['user_messages'].sum(),
                filtered_data['bot_messages'].sum()
            ]
        })
        fig = px.pie(
            message_data,
            values='count',
            names='type',
            title="Message Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Chat Activity
        daily_activity = filtered_data.groupby('date')['total_messages'].sum().reset_index()
        fig = px.line(
            daily_activity,
            x='date',
            y='total_messages',
            title="Daily Chat Activity"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Chat List
    st.subheader("Recent Chats")
    for _, chat in filtered_data.sort_values('created_at', ascending=False).head(5).iterrows():
        with st.expander(f"{chat['title']} ({chat['created_at'].strftime('%Y-%m-%d %H:%M')})"):
            st.write(f"Total Messages: {chat['total_messages']}")
            st.write(f"User Messages: {chat['user_messages']}")
            st.write(f"Bot Messages: {chat['bot_messages']}")

if __name__ == "__main__":
    main() 