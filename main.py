from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.handlers.search import search_router
from api.handlers.stream import stream_router
from settings import DOWNLOADS_DIR
import uvicorn, os

app = FastAPI(title='song_downloader')

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

main_api_router = APIRouter()

main_api_router.include_router(search_router, prefix="", tags=['search'])
main_api_router.include_router(stream_router, prefix="", tags=['stream'])

app.include_router(main_api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
 
if __name__ == "__main__":
  uvicorn.run("main:app", host="localhost", port=8090, reload=True, access_log=True)