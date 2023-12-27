from fastapi import FastAPI
from src.api import api_router
from src.auth.endpoints import router as auth_router

from fastapi.middleware.cors import CORSMiddleware


def create_app():
    _app = FastAPI(
        name="StroyVigoda",
        description="API",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )


    _app.include_router(api_router)
    _app.include_router(auth_router)
    return _app
