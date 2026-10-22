from langchain_core.tools import BaseTool

from backend.app.adapters.dto.mcp_client_tool import McpServerInfoDto
from backend.app.adapters.mcp_client_tool import McpClientTool
from backend.app.services.dto.user_mcp_tool import UserMcpServerCredDto
from backend.domain.enums.mcp_client import McpClientApp, McpClientAuthType
from backend.infra.tools.agni_mcp import AgniMcpClientTool
from backend.infra.tools.demo_mcp import DemoMcpClientTool


class SystemMcpClientTool(McpClientTool):
    def __init__(
            self, 
            agni_url: str
        ) -> None:
        self._agni_url = agni_url
        super().__init__()

    def list_mcp_server_info(self) -> list[McpServerInfoDto]:
        servers = [
            McpServerInfoDto(
                app=McpClientApp.DEMO_APP,
                auth_type=McpClientAuthType.NONE
            ),
            McpServerInfoDto(
                app=McpClientApp.AGNI_APP,
                auth_type=McpClientAuthType.API_KEY,
            ),
        ]

        return servers

    def get_mcp_tool(self, mcp_tool_app: McpClientApp, cred: UserMcpServerCredDto | None = None) -> BaseTool | None:
        if mcp_tool_app == McpClientApp.AGNI_APP:
            return AgniMcpClientTool(
                mcp_server_url=self._agni_url, 
                # api_key=cred.api_key when ready
            )
        elif mcp_tool_app == McpClientApp.DEMO_APP:
            return DemoMcpClientTool()
        
        return None