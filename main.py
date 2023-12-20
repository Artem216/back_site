import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app import create_app


app = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9999, host="0.0.0.0")

