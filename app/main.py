from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.deconvolution import router as parsing_router
from app.core.config import ORIGINS

app = FastAPI(
    title="Система для деконволюции изображений",
    description="Деконволюция - процесс, в ходе которого искажения вносимые оптической системой математически корректируются. "
                "Система помогает улучшать изображения.",
    version="1.2.3",
    contact={
        "name": "МФТИ",
        "url": "https://mipt.ru",
        "email": "digitaldepartments@mipt.ru",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    })

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(parsing_router, prefix="/deconvolution", tags=["deconvolution"])
