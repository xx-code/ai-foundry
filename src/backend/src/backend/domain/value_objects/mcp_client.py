
from dataclasses import dataclass

@dataclass(frozen=True)
class McpClientCred:
    encrypt_api_key: str | None = None