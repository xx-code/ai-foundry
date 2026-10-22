from datetime import datetime
from uuid import UUID

from backend.domain.entities.entity import Entity
from backend.domain.enums.mcp_client import McpClientApp
from backend.domain.value_objects.mcp_client import McpClientCred


class UserMcpServer(Entity):
    def __init__(
            self, 
            user_id: UUID,
            server_app: McpClientApp,
            client_cred: McpClientCred,
            id: UUID | None = None, 
            created_at: datetime | None = None, 
            updated_at: datetime | None = None):
        super().__init__(id, created_at, updated_at)

        self._user_id = user_id
        self._client_cred = client_cred
        self._server_app = server_app

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def client_cred(self) -> McpClientCred | None:
        return self._client_cred

    def set_client_cred(self, client_cred: McpClientCred):
        if self._client_cred != client_cred:
            self._client_cred =client_cred
            self._mark_changed()

    @property
    def server_app(self) -> McpClientApp:
        return self._server_app
 
