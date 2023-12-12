import requests
import json
import pandas as pd

URL_SPOTIFY_BASE = "https://api.spotify.com/v1/"

URL_SPOTIFY_MARKETS = URL_SPOTIFY_BASE + "markets"

URL_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"

URL_TRACKS = URL_SPOTIFY_BASE + 'artists/1Xyo4u8uXC1ZmMpatF05PJ/top-tracks'

data = {
    "grant_type": "client_credentials",
    "client_id": "8aa217ba6aa641ba9999fc9383cfe260",
    "client_secret": "0e8f0ab115e24fdba239455799da14f1"
}

response = requests.post(URL_SPOTIFY_TOKEN, data=data)

token = response.json().get('access_token')

print(token)

headers = {
    'Authorization': 'Bearer {}'.format(token)
}

responseMarkets = requests.get(URL_SPOTIFY_MARKETS, headers=headers)

markets = responseMarkets.json().get('markets')

lista = []

for market in markets:
    data = {
        "market": market
    }
    responseTracks = requests.get(URL_TRACKS, params=data, headers=headers)
    responseJSON = responseTracks.json()
    tracks = responseJSON.get('tracks')
    for track in tracks:
        temp = {}
        temp['name'] = track.get('name')
        print(temp['name'])
        temp['market'] = market
        print(temp['market'])
        temp['popularity'] = track.get('popularity')
        print(temp['popularity'])
        lista.append(temp)


df = pd.DataFrame(lista)
df.to_csv("topMusics.csv", index=False)