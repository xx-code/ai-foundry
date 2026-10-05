from typing import Protocol


class TokenAdapter(Protocol):
    def create_access_token(self, subject: str) -> str: ...

    def verify(self, token: str) -> str:
        """Retourne le `sub` du token, ou lève UnAuthorizedException."""
        ...