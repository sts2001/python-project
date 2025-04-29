from pydantic import BaseModel


class RegistrationModel(BaseModel):
    username: str
    password: str
    retyped_password: str
    email: str


class RegistrationSuccessModel(BaseModel):
    id: str
    username: str
    email: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str

