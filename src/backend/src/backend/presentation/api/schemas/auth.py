from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    user_name: str = Field(min_length=3, max_length=30)
    external_id: str = Field(max_length=100)
    password: str = Field(max_length=128)  # upper bound: avoids absurd hash costs


class LoginRequest(BaseModel):
    email_or_user_name: str
    password: str


class CreatedResponse(BaseModel):
    id: str


class UserResponse(BaseModel):
    id: str
    email: str
    user_name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"