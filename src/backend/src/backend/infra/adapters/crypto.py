from backend.app.adapters.crypto import Crypto
from cryptography.fernet import Fernet

class CryptoAdpater(Crypto):
    def __init__(self, secret_key: str) -> None:
        self.cipher = Fernet(secret_key.encode())

    def encrypt(self, value: str) -> str:
        encrypted_bytes = self.cipher.encrypt(value.encode("utf-8"))
        return encrypted_bytes.decode("utf-8")

    def decrypt(self, encrypt_value: str) -> str:
        decrypted_bytes = self.cipher.decrypt(encrypt_value.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
        
