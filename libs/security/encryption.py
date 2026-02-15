from cryptography.fernet import Fernet
import os
import base64

# Key generation: Fernet.generate_key()
# In production, this must be a persistent secret loaded from env/secrets manager
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())

cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def encrypt(data: str) -> str:
    """Encrypt a string."""
    if not data:
        return ""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    """Decrypt a string."""
    if not data:
        return ""
    return cipher_suite.decrypt(data.encode()).decode()
