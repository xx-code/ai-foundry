import uuid

from ...domain.entities.user import User
from ...domain.entities.user_password import UserPassword
from ...domain.repositories.user_password_repository import UserPasswordRepository
from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.unit_of_work import UnitOfWork
from ...domain.exception import AlreadyExistException, ValidationException, NotFoundException, UnAuthorizedException
from ..adapters.password_hasher import PasswordHasher
from .dto.base import CreatedDto
from .dto.user import UserRegisterDto, GetUserDto
from .dto.base import Result

class UserService:

    def __init__(
            self, 
            user_repo: UserRepository,
            user_pwd_repo: UserPasswordRepository,
            hash_crypto: PasswordHasher,
            uow: UnitOfWork
        ) -> None:
        self._user_repo = user_repo
        self._user_pwd_repo = user_pwd_repo
        self._hash_crypto = hash_crypto
        self._uow = uow

    def verify_password_valid(self, pwd: str):
        """
            Verify if the password is valid min 6 characteres with special case
            if not Raise ValidationException("PASSWORD_INVALID", "le mot de pass est invalid")
        """
        if len(pwd) < 6:
            raise ValidationException(
                "PASSWORD_INVALID",
                "Le mot de passe doit contenir au moins 6 caractères"
            )

        if not any(c.isupper() for c in pwd):
            raise ValidationException(
                "PASSWORD_INVALID",
                "Le mot de passe doit contenir au moins une majuscule"
            )

        if not any(not c.isalnum() for c in pwd):
            raise ValidationException(
                "PASSWORD_INVALID",
                "Le mot de passe doit contenir au moins un caractère spécial"
            )

    def register_new_user(self, new_user: UserRegisterDto) -> Result[CreatedDto]:
        try:
            if self._user_repo.get_by_email_or_user_name(new_user.user_name) is not None:
                raise AlreadyExistException("USER_ALREADY_EXIST", "l'utilisateur existe deja") 

            if self._user_repo.get_by_email_or_user_name(new_user.email) is not None:
                raise AlreadyExistException("USER_ALREADY_EXIST", "l'emeail existe deja") 

            self.verify_password_valid(new_user.password)
            pwd_hash = self._hash_crypto.crypt(new_user.password)

            created_user = User(email=new_user.email, user_name=new_user.user_name, external_id=new_user.external_id)

            self._user_repo.create(created_user)
            created_user_password = UserPassword(user_id=created_user.id, hashed_pwd=pwd_hash)
            self._user_pwd_repo.create(created_user_password)

            self._uow.commit()

            return Result.success(CreatedDto(id=str(created_user.id)))
        except Exception as e:
            self._uow.rollback()
            return Result.fail(e)


    def login_user(self, email_or_user_name: str, password: str) -> Result[GetUserDto]:
        try:
            user = self._user_repo.get_by_email_or_user_name(email_or_user_name)
            if user is None: 
                raise UnAuthorizedException("UNAUTHORIZE_USER", "Mauvais credential")

            user_password = self._user_pwd_repo.get_by_user_id(user.id)
            if user_password is None: 
                raise UnAuthorizedException("UNAUTHORIZE_USER", "Mauvais credential")

            if self._hash_crypto.verify(pwd=password, hashed=user_password.hashed_pwd) == False:
                raise UnAuthorizedException("UNAUTHORIZE_USER", "Mauvais credential")

            return Result.success(GetUserDto(id=str(user.id), email=user.email, user_name=user.user_name))
        except Exception as e:
            return Result.fail(e)

    def fetch_user(self, id: str) -> Result[GetUserDto]:
        try:
            user = self._user_repo.get(uuid.UUID(id))
            if user == None: 
                raise NotFoundException("USER_NOT_FOUND", "l'utilisateur est introuvable")

            user_dto = GetUserDto(id=str(user.id), email=user.email, user_name=user.user_name)

            return Result.success(user_dto)
        except Exception as e:
            return Result.fail(e) 