import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIFY_API_URL = "https://api.spotify.com/v1"

def get_access_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to fetch access token")

def get_artist_song(artist_name):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": artist_name, "type": "track", "limit": 10}
    response = requests.get(f"{SPOTIFY_API_URL}/search", headers=headers, params=params)
    tracks = response.json().get("tracks", {}).get("items", [])
    if tracks:
        return tracks[0]  # 랜덤 추천 가능
    return {"message": f"No songs found for artist: {artist_name}"}

def search_artist_song(artist_name):
    access_token = get_access_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": f'artist:"{artist_name}"',  # 아티스트 필드에서만 검색
        "type": "track",                # 곡 검색
        "limit": 5                      # 최대 5개의 곡 반환
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("tracks", {}).get("items", [])
        
        if not tracks:
            return {"message": "No tracks found for this artist"}
        
        result = []
        for track in tracks:
            result.append({
                "name": track["name"],                       # 곡 이름
                "artist": track["artists"][0]["name"],       # 아티스트 이름
                "url": track["external_urls"]["spotify"]    # Spotify URL
            })
        return {"results": result}
    else:
        return {"error": response.json()}