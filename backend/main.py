from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from spotify_api import get_artist_song, search_artist_song

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Spotify Music Recommendation API"}

@app.get("/artist")
def artist(artist_name: str):
    return get_artist_song(artist_name)

@app.get("/search")
def search(artist: str):
    return search_artist_song(artist)