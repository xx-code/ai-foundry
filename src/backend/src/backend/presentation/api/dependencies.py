from functools import lru_cache
from typing import Annotated, Iterator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.adapters.password_hasher import PasswordHasher
from backend.app.adapters.token_adapter import TokenAdapter
from backend.app.services.user import UserService
from backend.domain.repositories.unit_of_work import UnitOfWork
from backend.domain.repositories.user_password_repository import UserPasswordRepository
from backend.domain.repositories.user_repository import UserRepository
from backend.infra.adapters.jwt_token_adapter import JwtTokenService
from backend.infra.config import Settings, get_settings
from backend.infra.adapters.password_hasher import ScryptPasswordHasher
from backend.infra.persistence.sqlalchemy.database import Database
from backend.infra.persistence.sqlalchemy.repositories.user import SqlAlchemyUserRepository
from backend.infra.persistence.sqlalchemy.repositories.user_password import (
    SqlAlchemyUserPasswordRepository,
)
from backend.infra.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- Singletons (one per process): engine/pool and stateless hasher -----------
@lru_cache
def get_database() -> Database:
    settings: Settings = get_settings()
    return Database(create_engine(settings.database_url, pool_pre_ping=True))


@lru_cache
def get_password_hasher() -> ScryptPasswordHasher:
    return ScryptPasswordHasher()


@lru_cache
def get_token_adapter() -> TokenAdapter:
    s = get_settings()
    return JwtTokenService(s.jwt_secret, s.jwt_algorithm, s.jwt_expire_minutes)

DatabaseDep = Annotated[Database, Depends(get_database)]
HasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]
TokenAdapterDep =Annotated[TokenAdapter, Depends(get_token_adapter)]


# --- Cheap objects, built per request (the session lives in Database's ContextVar)
def get_session(db: DatabaseDep) -> Iterator[Session]:
    session = db.session_factory()
    try:
        yield session
    finally:
        session.close()  # annule automatiquement tout ce qui n'a pas été commité

SessionDep = Annotated[Session, Depends(get_session)]

def get_user_repository(session: SessionDep) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def get_user_password_repository(session: SessionDep) -> UserPasswordRepository:
    return SqlAlchemyUserPasswordRepository(session)



def get_uow(session: SessionDep) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)

def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    tokens: TokenAdapterDep 
) -> str: 
    return tokens.verify(token)

CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]


def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_pwd_repo: Annotated[UserPasswordRepository, Depends(get_user_password_repository)],
    hasher: HasherDep,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> UserService:
    return UserService(user_repo, user_pwd_repo, hasher, uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]