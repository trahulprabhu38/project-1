from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from dotenv import load_dotenv
import base64
import hashlib
from datetime import datetime
import uuid

load_dotenv()

# Default encryption key (64 characters)
DEFAULT_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

def get_encryption_key():
    # Get encryption key from environment variable or use default
    encryption_key = os.getenv("ENCRYPTION_KEY", DEFAULT_KEY)
    
    # Ensure the key is 64 characters long (32 bytes)
    if len(encryption_key) != 64:
        raise ValueError("Encryption key must be 64 characters long")
    
    # Convert hex string to bytes
    return bytes.fromhex(encryption_key)

def encrypt_message(message):
    try:
        message_bytes = message.encode('utf-8')
        iv = os.urandom(16)
        cipher = AES.new(get_encryption_key(), AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(message_bytes, AES.block_size))
        combined = iv + encrypted
        return base64.b64encode(combined).decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return message

def decrypt_message(encrypted_message):
    try:
        combined = base64.b64decode(encrypted_message)
        iv = combined[:16]
        encrypted = combined[16:]
        cipher = AES.new(get_encryption_key(), AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return encrypted_message

def generate_anonymous_id(user_id: str) -> str:
    """Generate a consistent anonymous ID for a user"""
    salt = os.getenv("ANONYMIZATION_SALT", "default_salt")
    return hashlib.sha256((user_id + salt).encode()).hexdigest()[:16]

def anonymize_timestamp(timestamp: datetime) -> str:
    """Anonymize timestamp by rounding to nearest hour"""
    return timestamp.replace(minute=0, second=0, microsecond=0).isoformat() 