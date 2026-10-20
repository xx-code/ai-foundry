from functools import lru_cache
from typing import Annotated, Iterator

from cachetools import TTLCache

from backend.app.adapters.chat_temporal_session import ChatTemporalSession
from backend.app.services.chat import ChatService
from backend.domain.repositories.model_repository import ModelRepository
from backend.infra.adapters.chat_temporal_session import ChatTemporalSessionTTLCache
from backend.infra.persistence.sqlalchemy.repositories.model import SqlAlchemyModelRepository
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.adapters.audit_logger import AuditLogger
from backend.app.adapters.crypto import Crypto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.adapters.password_hasher import PasswordHasher
from backend.app.adapters.token_adapter import TokenAdapter
from backend.app.services.ai_provider_key import AiProviderKeyService
from backend.app.services.model import ModelService
from backend.app.services.user import UserService
from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.entities.audit import Audit
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork
from backend.domain.repositories.user_password_repository import UserPasswordRepository
from backend.domain.repositories.user_repository import UserRepository
from backend.infra.adapters.audit_logger_adapter import AuditLoggerAdapter
from backend.infra.adapters.crypto import CryptoAdpater
from backend.infra.adapters.jwt_token_adapter import JwtTokenService
from backend.infra.adapters.provider_model_adapter import FactoryProviderAiModelRepository
from backend.infra.config import Settings, get_settings
from backend.infra.adapters.password_hasher import ScryptPasswordHasher
from backend.infra.persistence.sqlalchemy.database import Database
from backend.infra.persistence.sqlalchemy.repositories.ai_provider import SqlAlchemyAiProviderkeyRepository
from backend.infra.persistence.sqlalchemy.repositories.audit import SqlAlchemyAuditRepository
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

@lru_cache
def get_crypto() -> Crypto:
    s = get_settings()
    return CryptoAdpater(s.crypt_secret)

@lru_cache
def get_ai_provider_model_repository() -> ProviderAiModelRepository: 
    return FactoryProviderAiModelRepository()

@lru_cache
def get_chat_session() -> TTLCache:
    return TTLCache(maxsize=100, ttl=86400)


DatabaseDep = Annotated[Database, Depends(get_database)]
HasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]
TokenAdapterDep = Annotated[TokenAdapter, Depends(get_token_adapter)]
CryptoDep = Annotated[Crypto, Depends(get_crypto)]
ChatSessionDep = Annotated[TTLCache, Depends(get_chat_session)]


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

def get_audit_logger_repository(session: SessionDep) -> Repository[Audit]:
    return SqlAlchemyAuditRepository(session)

def get_ai_provider_repository(sesion: SessionDep) -> Repository[AiProviderKey]: 
    return SqlAlchemyAiProviderkeyRepository(sesion)

def get_model_repository(session: SessionDep) -> ModelRepository:
    return SqlAlchemyModelRepository(session)

def get_uow(session: SessionDep) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)

def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    tokens: TokenAdapterDep 
) -> str: 
    return tokens.verify(token)

def get_audit_logger(audit_repo: Annotated[Repository[Audit], Depends(get_audit_logger_repository)]) -> AuditLogger:
    return AuditLoggerAdapter(audit_repo) 

def get_chat_temporal_session_cache(session: ChatSessionDep) -> ChatTemporalSession: 
    return ChatTemporalSessionTTLCache(session)

AuditLoggerDep = Annotated[AuditLogger, Depends(get_audit_logger)]
CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]

def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_pwd_repo: Annotated[UserPasswordRepository, Depends(get_user_password_repository)],
    hasher: HasherDep,
    audit_logger: Annotated[AuditLogger, Depends(get_audit_logger)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> UserService:
    return UserService(user_repo, user_pwd_repo, hasher, audit_logger, uow)

def get_ai_provider_key_service(
    ai_provider_key_repo: Annotated[Repository[AiProviderKey], Depends(get_ai_provider_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    crypto: CryptoDep,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> AiProviderKeyService:
    return AiProviderKeyService(
        ai_provider_key_repo=ai_provider_key_repo,
        user_repo=user_repo,
        crypto=crypto,
        uow=uow
    )

def get_model_service(
        provider_model_repository: Annotated[ProviderAiModelRepository, Depends(get_ai_provider_model_repository)],
        ai_provider_key_repo: Annotated[Repository[AiProviderKey], Depends(get_ai_provider_repository)],
        user_repo: Annotated[UserRepository, Depends(get_user_repository)],
        model_repo: Annotated[ModelRepository, Depends(get_model_repository)],
        crypto: CryptoDep,
        uow: Annotated[UnitOfWork, Depends(get_uow)],
    ) -> ModelService:
    return ModelService(
        model_adapter=provider_model_repository,
        model_repo=model_repo,
        ai_provider_key_repo=ai_provider_key_repo,
        user_repo=user_repo,
        crypto=crypto,
        uow=uow
    )

def get_chat_service(
        model_service: Annotated[ModelService, Depends(get_model_service)],
        ai_provider_key_service: Annotated[AiProviderKeyService, Depends(get_ai_provider_key_service)],
        cache_session: Annotated[ChatTemporalSession, Depends(get_chat_temporal_session_cache)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
    ):
    return ChatService(
        model_service=model_service,
        ai_provider_key_service=ai_provider_key_service,
        chat_temporal_session=cache_session,
        uow=uow
    )


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AiProviderKeyServiceDep = Annotated[AiProviderKeyService, Depends(get_ai_provider_key_service)]
ModelServiceDep = Annotated[ModelService, Depends(get_model_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]