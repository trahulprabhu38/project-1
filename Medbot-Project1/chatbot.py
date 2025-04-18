import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from db_handler import ChatDatabase

load_dotenv()

class ChatBot:
    def __init__(self):
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
        
    def get_bot_response(self, chat_id, user_input):
        try:
            # First save the user's message
            self.db.add_message(chat_id, "user", user_input)
            
            # Get conversation history from database
            history = self.db.get_chat_history(chat_id)
            
            # Create memory from history
            memory = ConversationBufferMemory()
            for msg in history:
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["content"])
                else:
                    memory.chat_memory.add_ai_message(msg["content"])
            
            # Create conversation chain
            conversation = ConversationChain(
                llm=self.llm,
                memory=memory,
                prompt=self.prompt_template,
                verbose=False
            )
            
            # Get response
            response = conversation.predict(input=user_input)
            
            # Save bot's response
            self.db.add_message(chat_id, "assistant", response)
            
            return response
        except Exception as e:
            print(f"Error in get_bot_response: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."
