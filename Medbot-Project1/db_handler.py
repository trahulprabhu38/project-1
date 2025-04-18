from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

class ChatDatabase:
    def __init__(self):
        try:
            self.client = MongoClient(os.getenv("MONGODB_URI"))
            self.db = self.client["medbot"]
            self.chats = self.db["chats"]
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def create_chat(self):
        try:
            chat_id = self.chats.insert_one({
                "created_at": datetime.now(),
                "messages": []
            }).inserted_id
            return str(chat_id)
        except Exception as e:
            print(f"Error creating chat: {e}")
            return None
    
    def add_message(self, chat_id, role, content):
        try:
            self.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {
                    "$push": {
                        "messages": {
                            "role": role,
                            "content": content,
                            "timestamp": datetime.now()
                        }
                    },
                    "$set": {
                        "updated_at": datetime.now()
                    }
                }
            )
        except Exception as e:
            print(f"Error adding message: {e}")
    
    def get_chat_history(self, chat_id):
        try:
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            return chat["messages"] if chat else []
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def get_all_chats(self):
        try:
            return list(self.chats.find({}, {"_id": 1, "created_at": 1, "updated_at": 1})
                       .sort([("updated_at", -1), ("created_at", -1)]))
        except Exception as e:
            print(f"Error getting all chats: {e}")
            return []
    
    def delete_chat(self, chat_id):
        try:
            self.chats.delete_one({"_id": ObjectId(chat_id)})
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False 