from typing import Protocol

class Crypto(Protocol):
    def encrypt(self, value: str) -> str: 
        """encrypt a api key and return plain text encoded"""
        ...

    def decrypt(self, encrypt_value: str) -> str: 
        """decripty an api key and return plain text decoded"""
        ...
