from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId
from encryption import encrypt, decrypt, generate_anonymous_id, anonymize_timestamp

load_dotenv()

class ChatDatabase:
    def __init__(self):
        try:
            self.client = MongoClient(os.getenv("MONGODB_URI"))
            self.db = self.client["medbot"]
            self.chats = self.db["chats"]
            self.analytics = self.db["analytics"]  # New collection for anonymized data
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def create_chat(self, user_id):
        try:
            # Generate anonymous chat ID
            chat_id = str(ObjectId())
            anonymous_id = generate_anonymous_id(chat_id)
            
            # Create chat with anonymized data
            self.chats.insert_one({
                "_id": ObjectId(chat_id),
                "user_id": user_id,  # Add user_id to chat
                "anonymous_id": anonymous_id,
                "created_at": datetime.now(),
                "messages": []
            })
            
            # Store analytics data
            self.analytics.insert_one({
                "anonymous_id": anonymous_id,
                "user_id": user_id,  # Add user_id to analytics
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
            # Encrypt the message content
            encrypted_content = encrypt(content)
            
            # Get anonymous ID
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            anonymous_id = chat.get("anonymous_id")
            
            # Update chat with encrypted message
            self.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {
                    "$push": {
                        "messages": {
                            "role": role,
                            "content": encrypted_content,
                            "timestamp": datetime.now()
                        }
                    },
                    "$set": {
                        "updated_at": datetime.now()
                    }
                }
            )
            
            # Update analytics
            self.analytics.update_one(
                {"anonymous_id": anonymous_id},
                {
                    "$inc": {"message_count": 1},
                    "$set": {"last_activity": anonymize_timestamp(datetime.now())}
                }
            )
        except Exception as e:
            print(f"Error adding message: {e}")
    
    def get_chat_history(self, chat_id):
        try:
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            if chat and "messages" in chat:
                # Decrypt all messages
                decrypted_messages = []
                for msg in chat["messages"]:
                    try:
                        decrypted_content = decrypt(msg["content"])
                        decrypted_messages.append({
                            "role": msg["role"],
                            "content": decrypted_content,
                            "timestamp": msg["timestamp"]
                        })
                    except Exception as e:
                        print(f"Error decrypting message: {e}")
                        # If decryption fails, use the original content
                        decrypted_messages.append({
                            "role": msg["role"],
                            "content": msg["content"],
                            "timestamp": msg["timestamp"]
                        })
                return decrypted_messages
            return []
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def get_all_chats(self, user_id):
        try:
            # Return only anonymized data for the specific user
            return list(self.chats.find(
                {"user_id": user_id},  # Filter by user_id
                {
                    "_id": 1,
                    "anonymous_id": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "message_count": {"$size": "$messages"}
                }
            ).sort([("updated_at", -1), ("created_at", -1)]))
        except Exception as e:
            print(f"Error getting all chats: {e}")
            return []
    
    def delete_chat(self, chat_id):
        try:
            # Get anonymous ID before deletion
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            anonymous_id = chat.get("anonymous_id")
            
            # Delete chat
            self.chats.delete_one({"_id": ObjectId(chat_id)})
            
            # Remove analytics data
            self.analytics.delete_one({"anonymous_id": anonymous_id})
            
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False 