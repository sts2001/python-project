from fastapi import (APIRouter,
                     Depends,
                     status)
from fastapi.responses import (JSONResponse,
                               HTMLResponse)

from app.api.dependencies import (get_database,
                                  get_deconvolutioner)
from app.core.security import (o_auth2,
                               decode_token)
from app.database.postgres import Database
from app.deconvolution.frt import Deconvolution
from app.models.deconvolution import (DeconvolutionOutputData,
                                      DeconvolutionInputData,
                                      Results)

router = APIRouter()


@router.post("/calculate")
async def calculate(data: DeconvolutionInputData,
                    token: str = Depends(o_auth2),
                    database: Database = Depends(get_database),
                    deconvolution: Deconvolution = Depends(get_deconvolutioner)):
    payload = decode_token(token)
    if payload:
        if len(data.base64_img) == 0 or not data.base64_img.startswith("data:image/"):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Некорректные данные"}
            )
        job_id = database.add_job("В процессе",
                                  data.base64_img,
                                  payload["user_id"])
        image_base64 = deconvolution.get(data.base64_img)
        result_id = database.add_result(job_id,
                                        payload["user_id"],
                                        image_base64)
        database.update_job_status(job_id, "Завершено")
        return DeconvolutionOutputData(job_id=job_id,
                                       result_id=result_id,
                                       base64_img=image_base64)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )


@router.get("/watch/{result_id}")
async def watch(result_id: int,
                token: str = Depends(o_auth2),
                database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        result = database.get_result_data(result_id)
        if result:
            if result["user_id"] == payload["user_id"]:
                html_content = f"""
                    <html>
                        <body>
                            <h2>Base64 image:</h2>
                            <img src="{result['img']}" width="900">
                        </body>
                    </html>
                    """
                return HTMLResponse(
                    content=html_content
                )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Доступ запрещен"}
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Результат не найден"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )


@router.delete("/delete_result/{result_id}")
async def delete_result(result_id: int,
                        token: str = Depends(o_auth2),
                        database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        result = database.get_result_data(result_id)
        if result:
            if result["user_id"] == payload["user_id"]:
                if database.delete_result(result_id):
                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"detail": f"Результат удален"}
                    )
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": f"Ошибка сервера"}
                )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Доступ запрещен"}
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Результат не найден"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )


@router.get("/results")
async def get_results(token: str = Depends(o_auth2),
                      database: Database = Depends(get_database)):
    payload = decode_token(token)
    if payload:
        results = database.get_all_results(payload["user_id"])
        return Results(ids=[i["id"] for i in results])
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Пользователь не авторизован"}
    )
