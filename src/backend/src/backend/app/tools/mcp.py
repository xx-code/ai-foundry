from langchain_core.tools import BaseTool
from pydantic import Field

class McpClientTool(BaseTool):
    name: str = "mcp_client_tool"
    description: str = "Communique with MCP server via FastMCP."
    mcp_server_url: str = Field(description="URL server MCP (ex: SSE endpoint ou HTTP)")