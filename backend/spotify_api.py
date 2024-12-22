import os
import requests
import base64
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIFY_API_URL = "https://api.spotify.com/v1"

def get_access_token():
    """Spotify의 클라이언트 자격 증명 흐름을 사용하여 액세스 토큰 생성"""

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
    response.raise_for_status()
    return response.json()["access_token"]

def get_artist_song(artist_name):
    """주어진 아티스트의 랜덤 추천 곡 하나 가져오기"""

    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": artist_name, "type": "track", "limit": 20}
    
    response = requests.get(f"{SPOTIFY_API_URL}/search", headers=headers, params=params)
    response.raise_for_status()
    
    tracks = response.json().get("tracks", {}).get("items", [])
    if tracks:
        return tracks[0]
    return {"message": f"No songs found for artist: {artist_name}"}

def search_artist_song(artist_name):
    """특정 아티스트의 곡 검색, 20곡 요청 후 10곡만 반환"""
    
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": f'artist:"{artist_name}"',
        "type": "track",
        "limit": 20
    }
    
    response = requests.get(f"{SPOTIFY_API_URL}/search", headers=headers, params=params, timeout=10)
    response.raise_for_status()
    
    tracks = response.json().get("tracks", {}).get("items", [])
    if not tracks:
        return {"message": "No tracks found for this artist"}
    
    unique_tracks = {}
    for track in tracks:
        track_name = track["name"]
        if track_name not in unique_tracks:
            unique_tracks[track_name] = {
                "name": track_name,
                "artist": track["artists"][0]["name"],
                "url": track["external_urls"]["spotify"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"]
            }
    
    unique_tracks_list = list(unique_tracks.values())
    return {"results": unique_tracks_list[:10]}