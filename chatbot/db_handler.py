from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId
from encryption import encrypt_message, decrypt_message, generate_anonymous_id, anonymize_timestamp

load_dotenv()

class ChatDatabase:
    def __init__(self):
        try:
            self.client = MongoClient(os.getenv("MONGODB_URI"))
            self.db = self.client["medbot"]
            self.chats = self.db["chats"]
            self.analytics = self.db["analytics"]  
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def create_chat(self, user_id):
        try:
            chat_id = str(ObjectId())
            anonymous_id = generate_anonymous_id(chat_id)
            chat_doc = {
                "_id": ObjectId(chat_id),
                "user_id": user_id,
                "anonymous_id": anonymous_id,
                "title": "New Chat",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "messages": []
            }
        
            self.chats.insert_one(chat_doc)
            self.analytics.insert_one({
                "anonymous_id": anonymous_id,
                "user_id": user_id,
                "created_at": anonymize_timestamp(datetime.now()),
                "message_count": 0,
                "last_activity": anonymize_timestamp(datetime.now())
            })
            
            return chat_id
        except Exception as e:
            print(f"Error creating chat: {e}")
            return None
    
    def add_message(self, chat_id, role, content):
        try:
            encrypted_content = encrypt_message(content)
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            anonymous_id = chat.get("anonymous_id")
            message = {
                "role": role,
                "content": encrypted_content,
                "timestamp": datetime.now()
            }
        
            self.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {
                    "$push": {"messages": message},
                    "$set": {
                        "updated_at": datetime.now(),
                        "title": content[:40] + "..." if role == "user" and len(content) > 40 else chat.get("title", "New Chat")
                    }
                }
            )
            
            self.analytics.update_one(
                {"anonymous_id": anonymous_id},
                {
                    "$inc": {"message_count": 1},
                    "$set": {"last_activity": anonymize_timestamp(datetime.now())}
                }
            )
            
            return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_chat_history(self, chat_id):
        try:
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            if chat and "messages" in chat:
                decrypted_messages = []
                for msg in chat["messages"]:
                    try:
                        decrypted_content = decrypt_message(msg["content"])
                        decrypted_messages.append({
                            "role": msg["role"],
                            "content": decrypted_content,
                            "timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M") if "timestamp" in msg else None
                        })
                    except Exception as e:
                        print(f"Error decrypting message: {e}")
                        decrypted_messages.append({
                            "role": msg["role"],
                            "content": msg["content"],
                            "timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M") if "timestamp" in msg else None
                        })
                return decrypted_messages
            return []
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def get_all_chats(self, user_id):
        try:
            chats = list(self.chats.find(
                {"user_id": user_id}
            ).sort([("updated_at", -1), ("created_at", -1)]))
            
            for chat in chats:
                chat["_id"] = str(chat["_id"])
                if "messages" in chat and chat["messages"]:
                    user_messages = [msg for msg in chat["messages"] if msg["role"] == "user"]
                    if user_messages:
                        first_msg = user_messages[0]
                        try:
                            decrypted_content = decrypt_message(first_msg["content"])
                            chat["title"] = decrypted_content[:40] + "..." if len(decrypted_content) > 40 else decrypted_content
                        except:
                            chat["title"] = "New Chat"
                    else:
                        chat["title"] = "New Chat"
                else:
                    chat["title"] = "New Chat"
                chat["message_count"] = len(chat.get("messages", []))
                if "created_at" in chat:
                    chat["created_at"] = chat["created_at"].strftime("%Y-%m-%d %H:%M")
                if "updated_at" in chat:
                    chat["updated_at"] = chat["updated_at"].strftime("%Y-%m-%d %H:%M")
            
            return chats
        except Exception as e:
            print(f"Error getting all chats: {e}")
            return []
    
    def delete_chat(self, chat_id):
        try:
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            anonymous_id = chat.get("anonymous_id")
            self.chats.delete_one({"_id": ObjectId(chat_id)})
            self.analytics.delete_one({"anonymous_id": anonymous_id})
            
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False 