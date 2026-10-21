import ipaddress
from datetime import datetime
from uuid import UUID

from backend.domain.entities.entity import Entity
from backend.domain.exception import ValidationException


class UserMcpServer(Entity):
    def __init__(
            self, 
            user_id: UUID,
            hostname: str,
            encrypt_api_key: str | None = None,
            id: UUID | None = None, 
            created_at: datetime | None = None, 
            updated_at: datetime | None = None):
        super().__init__(id, created_at, updated_at)

        self._user_id = user_id
        self._hostname = self._validate_hostname(hostname)
        self._encrypt_api_key = encrypt_api_key

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def hostname(self) -> str:
        return self._hostname

    def set_hostname(self, hostname: str):
        if hostname != self._hostname: 
            self._hostname = self._validate_hostname(hostname)
            self._mark_changed()

    @property
    def encrypt_api_key(self) -> str | None:
        return self._encrypt_api_key

    def set_encrypt_api_key(self, encrypt_api_key: str):
        if encrypt_api_key != self._encrypt_api_key: 
            self._encrypt_api_key = encrypt_api_key
            self._mark_changed()   

    @staticmethod
    def _validate_hostname(hostname: str) -> str:
        error = ValidationException(
            "INVALID_MCP_SERVER_HOSTNAME",
            "MCP server hostname must be a valid hostname or IP address",
        )
        if not isinstance(hostname, str) or not hostname:
            raise error

        try:
            return str(ipaddress.ip_address(hostname))
        except ValueError:
            pass

        try:
            ascii_hostname = hostname.encode("idna").decode("ascii").lower()
        except UnicodeError:
            raise error from None

        has_trailing_dot = ascii_hostname.endswith(".")
        if has_trailing_dot:
            ascii_hostname = ascii_hostname[:-1]

        if (
            not ascii_hostname
            or len(ascii_hostname) > 253
            or any(
                not label
                or len(label) > 63
                or label.startswith("-")
                or label.endswith("-")
                or not all(
                    char.isascii() and (char.isalnum() or char == "-")
                    for char in label
                )
                for label in ascii_hostname.split(".")
            )
        ):
            raise error

        return ascii_hostname + ("." if has_trailing_dot else "")