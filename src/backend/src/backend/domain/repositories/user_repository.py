from typing import Protocol
from ..entities.user import User
from .repository import Repository

class UserRepository(Repository[User], Protocol):
    def get_by_email_or_user_name(self, email_or_username: str) -> User | None:...