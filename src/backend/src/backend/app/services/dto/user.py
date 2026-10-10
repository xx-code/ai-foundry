from dataclasses import dataclass

@dataclass
class UserRegisterDto:
    email: str
    user_name: str
    external_id: str
    password: str


@dataclass
class GetUserDto:
    id: str
    email: str
    user_name: str