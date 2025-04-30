import datetime

from fastapi import (APIRouter,
                     Depends,
                     status)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.models.auth import (RegistrationModel,
                             RegistrationSuccessModel,
                             TokenModel)
from app.api.dependencies import get_database
from app.core.config import ACCESS_TOKEN_EXP
from app.core.security import (hash_password,
                               is_it_correct_password,
                               get_access_token)
from app.database.postgres import Database

router = APIRouter()


@router.post("/sign_up")
async def sign_up(data: RegistrationModel,
                  database: Database = Depends(get_database)):
    if not data.password == data.retyped_password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароли не совпадают"}
        )
    if not database.get_user_id(data.username):
        password_hash = hash_password(data.password)
        user_id = database.add_user(data.username,
                                    password_hash,
                                    data.email)
        if user_id:
            return RegistrationSuccessModel(id=str(user_id),
                                            username=data.username,
                                            email=data.email)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Ошибка сервера"}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Пользователь с таким логином уже зарегистрирован"}
    )


@router.post("/sign_in")
async def sign_in(data: OAuth2PasswordRequestForm = Depends(),
                  database: Database = Depends(get_database)):
    user_id = database.get_user_id(data.username)
    if user_id:
        user_data = database.get_user_data(user_id)
        if is_it_correct_password(user_data["password"],
                                  data.password):
            token_inner_data = {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=ACCESS_TOKEN_EXP)
            }
            token = get_access_token(token_inner_data)
            if token:
                return TokenModel(access_token=token,
                                  token_type="bearer")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Ошибка сервера"}
            )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Неверный пароль"}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Пользователь с таким логином не зарегистрирован"}
    )

