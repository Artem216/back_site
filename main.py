import uvicorn
from src.app import create_app
from fastapi.middleware.cors import CORSMiddleware


app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origins
    allow_credentials=True,
    allow_methods=["*"],  # Set this to the allowed HTTP methods
    allow_headers=["*"],  # Set this to the allowed headers
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9999, host="0.0.0.0")
