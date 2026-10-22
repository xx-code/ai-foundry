from dataclasses import dataclass

from backend.domain.enums.mcp_client import McpClientApp, McpClientAuthType


@dataclass
class McpServerInfoDto:
    app: McpClientApp
    auth_type: McpClientAuthType