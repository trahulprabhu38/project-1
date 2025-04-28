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
            self.analytics = self.db["analytics"]  # New collection for anonymized data
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def create_chat(self, user_id):
        try:
            # Generate chat ID
            chat_id = str(ObjectId())
            anonymous_id = generate_anonymous_id(chat_id)
            
            # Create chat document
            chat_doc = {
                "_id": ObjectId(chat_id),
                "user_id": user_id,
                "anonymous_id": anonymous_id,
                "title": "New Chat",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "messages": []
            }
            
            # Insert into database
            self.chats.insert_one(chat_doc)
            
            # Store analytics data
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
            # Encrypt the message content
            encrypted_content = encrypt_message(content)
            
            # Get anonymous ID
            chat = self.chats.find_one({"_id": ObjectId(chat_id)})
            anonymous_id = chat.get("anonymous_id")
            
            # Create message document
            message = {
                "role": role,
                "content": encrypted_content,
                "timestamp": datetime.now()
            }
            
            # Update chat with encrypted message
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
            
            # Update analytics
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
                # Decrypt all messages
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
                        # If decryption fails, use the original content
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
            # Get all chats for the user with their messages
            chats = list(self.chats.find(
                {"user_id": user_id}
            ).sort([("updated_at", -1), ("created_at", -1)]))
            
            # Process each chat
            for chat in chats:
                # Convert ObjectId to string
                chat["_id"] = str(chat["_id"])
                
                # Get the first user message for the title
                if "messages" in chat and chat["messages"]:
                    # Find first user message
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
                
                # Add message count
                chat["message_count"] = len(chat.get("messages", []))
                
                # Format dates
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