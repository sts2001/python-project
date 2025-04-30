from pydantic import (BaseModel,
                      EmailStr)


class ChangingUsername(BaseModel):
    new_username: str


class ChangingPassword(BaseModel):
    previous: str
    new: str
    new_retyped: str


class UserData(BaseModel):
    user_id: int
    username: str
    email: EmailStr
