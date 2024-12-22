from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from spotify_api import get_artist_song, search_artist_song
from mangum import Mangum
import os

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=FileResponse)
def home():
    # ../frontend/index.html 파일 경로
    file_path = os.path.join(os.path.dirname(__file__), '../frontend/index.html')
    return FileResponse(file_path)

@app.get("/artist")
def artist(artist_name: str):
    return get_artist_song(artist_name)

@app.get("/search")
def search(artist: str):
    return search_artist_song(artist)