from fastapi import FastAPI
from spotify_api import get_artist_song, search_artist_song

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Spotify Music Recommendation API"}

@app.get("/artist")
def artist(artist_name: str):
    return get_artist_song(artist_name)

@app.get("/search")
def search(artist: str):
    result = search_artist_song(artist)
    return result