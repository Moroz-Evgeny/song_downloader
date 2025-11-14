from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.handlers.search import search_router
from api.handlers.stream import stream_router
from settings import DOWNLOADS_DIR
from html_content import html_content
import uvicorn, os

app = FastAPI(title='song_downloader')

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

main_api_router = APIRouter()

main_api_router.include_router(search_router, prefix="", tags=['search'])
main_api_router.include_router(stream_router, prefix="", tags=['stream'])

app.include_router(main_api_router)

@app.get("/")
async def serve_html():
    return HTMLResponse(html_content)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
 
if __name__ == "__main__":
  uvicorn.run("main:app", host="localhost", port=8080, reload=True, access_log=True)