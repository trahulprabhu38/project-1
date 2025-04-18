import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192",
    temperature=0.7
)

prompt_template = PromptTemplate(
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

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template,
    verbose=False
)

def get_bot_response(user_input):
    return conversation.predict(input=user_input)
