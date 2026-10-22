
from fastapi import APIRouter, Response, status

from backend.presentation.api.dependencies import (
    CurrentUserIdDep,
    McpClientToolDep,
    UserMcpServerServiceDep,
)
from backend.presentation.api.schemas.base import CreatedResponse, ListResponse
from backend.presentation.api.schemas.user_mcp_server import (
    AddUserMcpServerRequest,
    McpClientToolResponse,
    UpdateUserMcpServerRequest,
    UserMcpServerResponse,
)


router = APIRouter(prefix="/user-mcp-servers", tags=["user-mcp-servers"])

@router.get("/list-mcp-tools", response_model=ListResponse[McpClientToolResponse])
def list_mcp_tool(
    __: CurrentUserIdDep,
    adapter: McpClientToolDep,
) -> ListResponse[McpClientToolResponse]:
    mcps = adapter.list_mcp_server_info()
    return ListResponse(
        items=[McpClientToolResponse.from_adapter(item) for item in mcps],
        total=len(mcps)
    ) 

@router.get("/{mcp_id}", response_model=UserMcpServerResponse)
def get_mcp(
    mcp_id: str,
    user_id: CurrentUserIdDep,
    service: UserMcpServerServiceDep,
) -> UserMcpServerResponse:
    mcp = service.get_user_mcp_server(mcp_id, user_id).get_or_throw()
    return UserMcpServerResponse.from_service(mcp)


@router.get("", response_model=ListResponse[UserMcpServerResponse])
def get_mcps(
    user_id: CurrentUserIdDep,
    service: UserMcpServerServiceDep,
) -> ListResponse[UserMcpServerResponse]:
    mcps = service.get_mcp_servers(user_id).get_or_throw()
    return ListResponse(
        items=[UserMcpServerResponse.from_service(mcp) for mcp in mcps.items],
        total=mcps.total,
    )


@router.post(
    "",
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_mcp(
    user_id: CurrentUserIdDep,
    request: AddUserMcpServerRequest,
    service: UserMcpServerServiceDep,
) -> CreatedResponse:
    created = service.add_server(request.to_service(user_id)).get_or_throw()
    return CreatedResponse.from_service(created)


@router.put("/{mcp_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_mcp(
    mcp_id: str,
    user_id: CurrentUserIdDep,
    request: UpdateUserMcpServerRequest,
    service: UserMcpServerServiceDep,
) -> Response:
    service.update_server(request.to_service(mcp_id), user_id).get_or_throw()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{mcp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mcp(
    mcp_id: str,
    user_id: CurrentUserIdDep,
    service: UserMcpServerServiceDep,
) -> Response:
    service.delete_mcp_server(mcp_id, user_id).get_or_throw()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
