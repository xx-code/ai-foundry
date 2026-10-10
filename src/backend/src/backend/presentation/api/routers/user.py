from fastapi import APIRouter

from backend.presentation.api.dependencies import UserServiceDep, CurrentUserIdDep
from backend.presentation.api.schemas.auth import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, _: CurrentUserIdDep, service: UserServiceDep) -> UserResponse:
    user = service.fetch_user(user_id).get_or_throw()
    return UserResponse(id=user.id, email=user.email, user_name=user.user_name)

