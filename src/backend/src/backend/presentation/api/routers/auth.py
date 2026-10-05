from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.services.dto.user import UserRegisterDto  # adapt to your path
from backend.presentation.api.dependencies import UserServiceDep, TokenAdapterDep, CurrentUserIdDep
from backend.presentation.api.schemas.auth import (
    CreatedResponse,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=CreatedResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, service: UserServiceDep) -> CreatedResponse:
    dto = UserRegisterDto(
        email=body.email,
        user_name=body.user_name,
        external_id=body.external_id,
        password=body.password,
    )
    created = service.register_new_user(dto).get_or_throw()  # a Failure is raised -> handled globally
    return CreatedResponse(id=created.id)

@router.post("/login", response_model=LoginResponse)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
    tokens: TokenAdapterDep,
) -> LoginResponse:
    # OAuth2 impose le nom de champ "username" : on y met email OU user_name
    user = service.login_user(form.username, form.password).get_or_throw()
    return LoginResponse(access_token=tokens.create_access_token(subject=user.id))

@router.get("/me", response_model=UserResponse)
def get_me(user_id: CurrentUserIdDep, service: UserServiceDep) -> UserResponse:
    user = service.fetch_user(user_id).get_or_throw()
    return UserResponse(id=user.id, email=user.email, user_name=user.user_name)