from collections.abc import Callable

from backend.app.adapters.ai_code_interpretor_tool import AiCodeInterpretorTool
from backend.app.adapters.ai_web_tool import AiWebTool
from backend.app.services.dto.ai_tool import ToolSelectionDto
from backend.app.services.dto.base import Result
from backend.domain.entities.user_mcp_server import UserMcpServer
from backend.domain.enums.ai_tool import AiToolType
from backend.domain.repositories.repository import Repository
from langchain_core.tools import BaseTool


class AiToolService:
    def __init__(
            self,
            ai_web_tools: AiWebTool,
            ai_code_interpretor_tools: AiCodeInterpretorTool,
            user_mcp_server_repo: Repository[UserMcpServer]
        ) -> None:
        self._ai_web_tools = ai_web_tools
        self._ai_code_interpretor_tools = ai_code_interpretor_tools
        self._user_mcp_server_repo = user_mcp_server_repo

    def _fetch_mcp_tool(self, id: str) -> BaseTool:...


    def list_tools(self, selections: list[ToolSelectionDto]) -> Result[list[BaseTool]]:
        try:
            tool_factories: dict[
                AiToolType, tuple[Callable[[], BaseTool | None], ...]
            ] = {
                AiToolType.WEB_SEARCH: (
                    self._ai_web_tools.get_web_search_tool,
                    self._ai_web_tools.get_entities_tool,
                    self._ai_web_tools.get_knowledge_graph_tool,
                ),
                AiToolType.CODE_INTERPRETOR: (
                    self._ai_code_interpretor_tools.get_python_interpretor,
                    self._ai_code_interpretor_tools.get_python_interpretor_repl,
                    self._ai_code_interpretor_tools.get_js_interpretor,
                    self._ai_code_interpretor_tools.get_js_interpretor_repl,
                ),
            }

            tools: list[BaseTool] = []
            for selection in selections:
                if selection.tool_type == AiToolType.MCP_SERVER:
                    tool = self._fetch_mcp_tool(selection.tool_id)
                    tools.append(tool)
                    continue

                for create_tool in tool_factories[selection.tool_type]:
                    tool = create_tool()
                    if tool is not None:
                        tools.append(tool)

            return Result.success(tools)
        except Exception as e:
            return Result.fail(e)
        