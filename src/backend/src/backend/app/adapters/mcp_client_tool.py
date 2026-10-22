from typing import Protocol

from langchain_core.tools import BaseTool

from backend.app.adapters.dto.mcp_client_tool import McpServerInfoDto
from backend.app.services.dto.user_mcp_tool import UserMcpServerCredDto
from backend.domain.enums.mcp_client import McpClientApp


class McpClientTool(Protocol):
    def list_mcp_server_info(self) -> list[McpServerInfoDto]:... 
    def get_mcp_tool(self, mcp_tool_app: McpClientApp, cred: UserMcpServerCredDto | None = None) -> BaseTool | None:...