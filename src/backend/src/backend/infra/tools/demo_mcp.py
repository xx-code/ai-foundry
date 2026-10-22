import asyncio

from fastmcp import Client, FastMCP
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field


demo_mcp_server = FastMCP("Demo MCP")


@demo_mcp_server.tool
def echo(message: str) -> str:
	return f"Demo MCP received: {message}"


class DemoMcpInput(BaseModel):
	message: str = Field(description="Message envoyé à l’outil MCP de démonstration")


class DemoMcpClientTool(BaseTool):
	name: str = "demo_mcp_client"
	description: str = "Appelle l’outil echo du serveur FastMCP de démonstration."
	args_schema: ArgsSchema | None = DemoMcpInput

	async def _call_mcp(self, message: str) -> str:
		async with Client(demo_mcp_server, auth=None) as client:
			result = await client.call_tool("echo", {"message": message})

		if getattr(result, "isError", False):
			raise RuntimeError(f"Demo MCP call failed: {result.content}")

		text = [
			item_text
			for item in result.content
			if isinstance(item_text := getattr(item, "text", None), str)
		]
		if not text:
			raise RuntimeError("Demo MCP returned no text content")
		return "\n".join(text)

	def _run(self, message: str) -> str:
		return asyncio.run(self._call_mcp(message))

	async def _arun(self, message: str) -> str:
		return await self._call_mcp(message)
