import uuid

from backend.app.adapters.crypto import Crypto
from backend.app.queries.comparator import Comparator
from backend.app.queries.condition import Condition
from backend.app.queries.query import Query
from backend.app.services.dto.base import CreatedDto, ListDto, Result
from backend.app.services.dto.user_mcp_tool import (
    AddUserMcpServerDto,
    UpdateUserMcpServerDto,
    UserMcpServerCredDto,
    UserMcpServerDto,
)
from backend.domain.entities.user import User
from backend.domain.entities.user_mcp_server import UserMcpServer
from backend.domain.value_objects.mcp_client import McpClientCred
from backend.domain.exception import ForbiddenException, NotFoundException
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork



class UserMcpToolServerService:

    def __init__(
            self,
            user_repo: Repository[User],
            user_mcp_tool_repo: Repository[UserMcpServer],
            crypto: Crypto,
            uow: UnitOfWork) -> None:
        self._user_repo = user_repo
        self._user_mcp_tool_repo = user_mcp_tool_repo
        self._crypto = crypto
        self._uow = uow


    def add_server(self, input: AddUserMcpServerDto) -> Result[CreatedDto]:
        try:
            user_id = uuid.UUID(input.user_id) 
            user = self._user_repo.get(user_id)
            if user == None: 
                raise NotFoundException("USER_NOT_FOUND", "l'utilisateur est introuvable")

            encrypt_api_key = (
                self._crypto.encrypt(input.api_key)
                if input.api_key is not None
                else None
            )

            new_user_mcp = UserMcpServer(
                user_id=user_id,
                server_app=input.app,
                client_cred=McpClientCred(encrypt_api_key=encrypt_api_key),
            )

            self._user_mcp_tool_repo.create(new_user_mcp)

            self._uow.commit()

            return Result.success(CreatedDto(str(new_user_mcp.id)))
        except Exception as e:
            return Result.fail(e)

    def update_server(
        self,
        input: UpdateUserMcpServerDto,
        user_id: str | None = None,
    ) -> Result[None]:
        try:
            mcp_id = uuid.UUID(input.id) 
            mcp = self._user_mcp_tool_repo.get(mcp_id)
            if mcp == None: 
                raise NotFoundException("USER_MCP_TOOL_NOT_FOUND", "mcp tool not found est introuvable")
            if user_id is not None and mcp.user_id != uuid.UUID(user_id):
                raise ForbiddenException("USER_MCP_FORBIDDEN")

            if input.api_key is not None:
                encrypt_api_key = self._crypto.encrypt(input.api_key)
                mcp.set_client_cred(McpClientCred(encrypt_api_key=encrypt_api_key))

            if mcp.has_changed:
                self._user_mcp_tool_repo.update(mcp)
                self._uow.commit()

            return Result.success(None)
        except Exception as e:
            return Result.fail(e)

    def get_mcp_servers(self, user_id: str) -> Result[ListDto[UserMcpServerDto]]:
        try:    
            user = self._user_repo.get(uuid.UUID(user_id))
            if user == None: 
                raise NotFoundException("USER_NOT_FOUND", "l'utilisateur est introuvable")

            mcps = self._user_mcp_tool_repo.get_all(Query(
                conditions=(Condition("user_id", Comparator.EQUAL, user.id),)
            ))

            items = []
            for item in mcps.items:
                cred = UserMcpServerCredDto.from_value_object(
                    item.client_cred,
                    self._crypto,
                )
                items.append(UserMcpServerDto.from_model(item, cred))
            
            return Result.success(ListDto(
                items=items,
                total=mcps.total
            ))
        except Exception as e:
            return Result.fail(e)

    def get_user_mcp_server(
        self,
        id: str,
        user_id: str | None = None,
    ) -> Result[UserMcpServerDto]:
        try:    
            mcp = self._user_mcp_tool_repo.get(uuid.UUID(id))
            if mcp == None: 
                raise NotFoundException("USER_MCP_TOOL_NOT_FOUND", "mcp tool not found est introuvable")
            if user_id is not None and mcp.user_id != uuid.UUID(user_id):
                raise ForbiddenException("USER_MCP_FORBIDDEN")

            cred = UserMcpServerCredDto.from_value_object(
                mcp.client_cred,
                self._crypto,
            )

            return Result.success(
                UserMcpServerDto.from_model(mcp, cred)
            )
        except Exception as e:
            return Result.fail(e)

    def delete_mcp_server(
        self,
        id: str,
        user_id: str | None = None,
    ) -> Result[None]:
        try:
            mcp = self._user_mcp_tool_repo.get(uuid.UUID(id))
            if mcp == None: 
                raise NotFoundException("USER_MCP_TOOL_NOT_FOUND", "mcp tool not found est introuvable")
            if user_id is not None and mcp.user_id != uuid.UUID(user_id):
                raise ForbiddenException("USER_MCP_FORBIDDEN")

            self._user_mcp_tool_repo.delete(id)
            self._uow.commit()

            return Result.success(None)
        except Exception as e:
            return Result.fail(e)