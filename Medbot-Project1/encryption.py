from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
import hashlib
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Default key if ENCRYPTION_KEY is not set
DEFAULT_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

# Get encryption key from environment or use default
encryption_key = os.getenv("ENCRYPTION_KEY", DEFAULT_KEY)
if len(encryption_key) != 64:
    raise ValueError("ENCRYPTION_KEY must be 64 hexadecimal characters long")

SECRET_KEY = bytes.fromhex(encryption_key)

def generate_anonymous_id(user_id: str) -> str:
    """Generate a consistent anonymous ID for a user"""
    salt = os.getenv("ANONYMIZATION_SALT", "default_salt")
    return hashlib.sha256((user_id + salt).encode()).hexdigest()[:16]

def anonymize_timestamp(timestamp: datetime) -> str:
    """Anonymize timestamp by rounding to nearest hour"""
    return timestamp.replace(minute=0, second=0, microsecond=0).isoformat()

def pad(data):
    pad_length = AES.block_size - len(data) % AES.block_size
    return data + chr(pad_length) * pad_length

def unpad(data):
    pad_length = ord(data[-1])
    return data[:-pad_length]

def encrypt(plain_text: str) -> str:
    try:
        iv = get_random_bytes(16)
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        padded_text = pad(plain_text)
        encrypted = cipher.encrypt(padded_text.encode('utf-8'))
        encrypted_data = base64.b64encode(iv + encrypted).decode('utf-8')
        return encrypted_data
    except Exception as e:
        print(f"Encryption error: {e}")
        return plain_text

def decrypt(encrypted_data: str) -> str:
    try:
        # Remove any existing padding characters
        encrypted_data = encrypted_data.rstrip('=')
        
        # Add back the correct padding
        padding = len(encrypted_data) % 4
        if padding:
            encrypted_data += '=' * (4 - padding)
            
        raw_data = base64.b64decode(encrypted_data)
        iv = raw_data[:16]
        encrypted = raw_data[16:]
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted).decode('utf-8')
        return unpad(decrypted)
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_data 