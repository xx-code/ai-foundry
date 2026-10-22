from enum import Enum

class McpClientAuthType(str, Enum):
    API_KEY="API_KEY"
    CREDIENTIAL="CREDENTIAL"
    NONE="NONE"

class McpClientApp(str, Enum):
    DEMO_APP="DEMO_APP"
    AGNI_APP="AGNI_APP"
