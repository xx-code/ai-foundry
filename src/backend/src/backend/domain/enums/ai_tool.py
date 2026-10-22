from enum import Enum


class AiToolType(str, Enum):
    WEB_SEARCH="WebSearch"
    CODE_INTERPRETOR="CodeInterpretor"
    MCP_SERVER="McpServer"