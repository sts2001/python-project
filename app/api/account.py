from fastapi import (APIRouter,
                     Depends,
                     status)
from fastapi.responses import JSONResponse

from app.api.dependencies import get_database
from app.core.security import (is_it_correct_password,
                               o_auth2,
                               decode_token)
from app.database.postgres import Database
from app.models.account import (ChangingUsername,
                                ChangingPassword,
                                UserData)

router = APIRouter()


@router.put("/change_username")
async def change_username(data: ChangingUsername,
                          token: str = Depends(o_auth2),
                          database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        if len(data.new_username) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Новое имя пользователя пусто"}
            )
        if database.change_user_username(payload["user_id"],
                                         data.new_username):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Имя пользователя изменено"}
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Ошибка сервера"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )


@router.put("/change_password")
async def change_password(data: ChangingPassword,
                          token: str = Depends(o_auth2),
                          database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        if data.new == data.new_retyped:
            if is_it_correct_password(database.get_user_data(payload["user_id"])["password"],
                                      data.previous):
                if database.change_user_password(payload["user_id"],
                                                 data.new):
                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"detail": f"Пароль был изменен"}
                    )
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": f"Ошибка сервера"}
                )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Старый пароль неверный либо новые не совпадают"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )


@router.get("/get_user_data")
async def get_user_data(token: str = Depends(o_auth2),
                        database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        user_data = database.get_user_data(payload["user_id"])
        if user_data:
            return UserData(user_id=user_data["id"],
                            username=user_data["username"],
                            email=user_data["email"])
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Ошибка сервера"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )


@router.delete("/delete_account")
async def delete_account(token: str = Depends(o_auth2),
                         database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        if database.delete_user(payload["user_id"]):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Аккаунт удален"}
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Ошибка сервера"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Пользователь не авторизован"}
    )
