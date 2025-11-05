from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.handlers import download_router
from settings import DOWNLOADS_DIR
import uvicorn, os

app = FastAPI(title='song_downloader')

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

main_api_router = APIRouter()

main_api_router.include_router(download_router, prefix="/download", tags=['download'])

app.include_router(main_api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
 
if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, access_log=True)