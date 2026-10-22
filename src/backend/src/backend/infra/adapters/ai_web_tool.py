from backend.app.adapters.ai_web_tool import AiWebTool
from diffbot import Diffbot
from langchain_core.tools import BaseTool
from langchain_diffbot import DiffbotEntitiesTool, DiffbotKnowledgeGraphTool, DiffbotWebSearchTool


class DiffBotAiWebTool(AiWebTool):
    def __init__(self, api_token: str) -> None:
        self._api_token = api_token

    def get_web_search_tool(self) -> BaseTool | None:
        tool = DiffbotWebSearchTool(client=Diffbot(token=self._api_token))
        return tool

    def get_knowledge_graph_tool(self) -> BaseTool | None:
        tool = DiffbotKnowledgeGraphTool(client=Diffbot(token=self._api_token))
        return tool

    def get_entities_tool(self) -> BaseTool | None:
        tool = DiffbotEntitiesTool(client=Diffbot(token=self._api_token))
        return tool

