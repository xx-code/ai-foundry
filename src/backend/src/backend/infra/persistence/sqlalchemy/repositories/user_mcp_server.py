from backend.domain.entities.user_mcp_server import UserMcpServer
from backend.infra.persistence.sqlalchemy.models.user_mcp_server import (
    UserMcpServerModel,
)
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyUserMcpServerRepository(
    SqlAlchemyRepository[UserMcpServer, UserMcpServerModel]
):
    model = UserMcpServerModel