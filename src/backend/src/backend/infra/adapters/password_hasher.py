import hashlib
import hmac
import os

from backend.app.adapters.password_hasher import PasswordHasher

class ScryptPasswordHasher(PasswordHasher):

    def __init__(self, n: int = 2**14, r: int = 8, p: int = 1) -> None:
        self._n, self._r, self._p = n, r, p

    def crypt(self, pwd: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.scrypt(
            pwd.encode(), salt=salt, n=self._n, r=self._r, p=self._p
        )
        return f"{salt.hex()}${digest.hex()}"

    def verify(self, pwd: str, hashed: str) -> bool:
        salt_hex, digest_hex = hashed.split("$")
        digest = hashlib.scrypt(
            pwd.encode(), salt=bytes.fromhex(salt_hex),
            n=self._n, r=self._r, p=self._p,
        )
        return hmac.compare_digest(digest, bytes.fromhex(digest_hex))
