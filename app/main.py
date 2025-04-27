from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import ORIGINS

app = FastAPI(
    title="Система для деконволюции изображений",
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

