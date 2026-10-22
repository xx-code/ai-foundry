import asyncio
from fastmcp import Client
from langchain_core.tools import BaseTool
from pydantic import Field, PrivateAttr
import requests

class AgniMcpClientTool(BaseTool):
    name: str = "mcp_client_tool"
    description: str = "Communique with MCP server via FastMCP."
    mcp_server_url: str = Field(description="URL server MCP (ex: SSE endpoint ou HTTP)")
    # api_key: dict|None = Field(default=None, description="The api token give by the provider of the server mcp can be {api_key: ....} if None is open access not auth")

    _cached_token: str | None = PrivateAttr(default=None)

    def _auth(self) -> str:
        ...
        # Not need for now
        # if self._cached_token:
        #     return self._cached_token

        # # here setup the system logger for the observability

        # res = requests.post(f"{self.mcp_server_url}{self.mcp_auth_endpoint}", json=self.api_key)
        # self._cached_token = res.json()["token"]

        # return self._cached_token or ""

    def _run(self, tool_name: str, args: dict) -> str:
        ...
        # if self.api_key is not None:
        #     self._auth()

        # async def run_fastmcp():
        #     async with Client(self.mcp_server_url) as client:
        #         result = await client.call_tool(
        #             name=tool_name,
        #             arguments=args
        #         )
        #         return result

        # try:
        #     loop = asyncio.get_running_loop()
        # except RuntimeError:
        #     loop =None

        # if loop and loop.is_running():
        #     pass

        # return asyncio.run(run_fastmcp())
