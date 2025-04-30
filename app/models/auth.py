from pydantic import BaseModel, EmailStr


class RegistrationModel(BaseModel):
    username: str
    password: str
    retyped_password: str
    email: EmailStr


class RegistrationSuccessModel(BaseModel):
    id: int
    username: str
    email: EmailStr


class TokenModel(BaseModel):
    access_token: str
    token_type: str

