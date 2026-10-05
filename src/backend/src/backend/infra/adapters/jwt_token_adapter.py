from datetime import UTC, datetime, timedelta

import jwt

from backend.domain.exception import UnAuthorizedException  # adapte le chemin


class JwtTokenService:
    def __init__(self, secret: str, algorithm: str = "HS256", expires_minutes: int = 60) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expires = timedelta(minutes=expires_minutes)

    def create_access_token(self, subject: str) -> str:
        now = datetime.now(UTC)
        payload = {"sub": subject, "iat": now, "exp": now + self._expires}  # type: ignore
        return jwt.encode(payload, self._secret, algorithm=self._algorithm) # type: ignore

    def verify(self, token: str) -> str:
        try:
            payload = jwt.decode( # type: ignore
                token,
                self._secret,
                algorithms=[self._algorithm],  #
                options={"require": ["exp", "sub"]},
            )
        except jwt.PyJWTError as e:
            raise UnAuthorizedException("INVALID_TOKEN", "Token invalide ou expiré") from e
        return payload["sub"]