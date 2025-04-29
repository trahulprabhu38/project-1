import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from db_handler import ChatDatabase
from encryption import encrypt_message, decrypt_message
from recommendation_system import MoodBasedRecommender

load_dotenv()

class ChatBot:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=os.getenv("GROQ_API_KEY"),
                model="llama3-8b-8192",
                temperature=0.7
            )
            
            self.prompt_template = PromptTemplate(
                input_variables=["history", "input"],
                template="""
You are an empathetic, supportive AI assistant focused on mental health and emotional well-being.

ONLY respond specifically to the user's query.
Avoid giving generic disclaimers like "I'm not a therapist" or "consult a professional".
Be warm, concise, and directly helpful.

Conversation so far:
{history}
User: {input}
AI:"""
            )
            
            self.db = ChatDatabase()
            
            # Initialize the recommendation system
            dataset_path = os.path.join(os.path.dirname(__file__), 'mental_health_chatbot_interactions.csv')
            self.recommender = MoodBasedRecommender(dataset_path)
            
        except Exception as e:
            print(f"Error initializing chatbot: {e}")
            raise

    @staticmethod
    def is_mood_message(user_input):
        mood_keywords = [
            'suggest', 'recommend', 'help', 'manage my', 'what should i do ', 'any tips for'
        ]
        user_input_lower = user_input.lower()
        return any(kw in user_input_lower for kw in mood_keywords)

    def get_bot_response(self, chat_id, user_input):
        try:
            if self.is_mood_message(user_input):
                if self.recommender:
                    recommendations = self.recommender.get_recommendations(user_input)
                    response = "Here are some exercises that might help you:\n\n"
                    for i, rec in enumerate(recommendations, 1):
                        response += f"{i}. {rec['exercise']}\n\n"
                    response += "Would you like to try any of these exercises? I'm here to support you."
                    return response
                else:
                    return "I apologize, but I'm having trouble accessing the recommendation system right now. Please try again later."
            # Otherwise, use LLM for normal conversation
            history = self.db.get_chat_history(chat_id)
            memory = ConversationBufferMemory()
            for msg in history:
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["content"])
                else:
                    memory.chat_memory.add_ai_message(msg["content"])
            conversation = ConversationChain(
                llm=self.llm,
                memory=memory,
                prompt=self.prompt_template,
                verbose=False
            )
            response = conversation.predict(input=user_input)
            return response
        except Exception as e:
            print(f"Error in get_bot_response: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."

def main():
    # Example usage
    chatbot = ChatBot()
    print("Welcome to the Mental Health Support Chat!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("\nTake care! Remember, you're not alone. 💚")
            break
            
        response = chatbot.get_bot_response("test_chat_id", user_input)
        print(f"\nBot: {response}")

if __name__ == "__main__":
    main()
