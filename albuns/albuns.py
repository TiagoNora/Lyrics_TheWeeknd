import requests
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv(dotenv_path="./v.env")
import os

URL_SPOTIFY_BASE = "https://api.spotify.com/v1/"

URL_SPOTIFY_MARKETS = URL_SPOTIFY_BASE + "markets"

URL_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"

URL_TRACKS = URL_SPOTIFY_BASE + 'artists/1Xyo4u8uXC1ZmMpatF05PJ/top-tracks'

URL_ALBUNS = URL_SPOTIFY_BASE + 'artists/1Xyo4u8uXC1ZmMpatF05PJ/albums'

print(os.environ.get("grant_type"))

data = {
    "grant_type": os.environ.get("grant_type"),
    "client_id": os.environ.get("client_id"),
    "client_secret": os.environ.get("client_secret")
}

response = requests.post(URL_SPOTIFY_TOKEN, data=data)

token = response.json().get('access_token')

print(token)

headers = {
    'Authorization': 'Bearer {}'.format(token)
}

responseMarkets = requests.get(URL_SPOTIFY_MARKETS, headers=headers)

markets = responseMarkets.json().get('markets')



dataAlbum = {
    "include_groups": "album",
    "market": "PT",
    "limit": "50",
    "offset": "0"
}

responseAlbuns = requests.get(URL_ALBUNS,headers=headers, params=dataAlbum)

albunsJson = responseAlbuns.json().get('items')
print(albunsJson)

albuns = []


lista = [
    'Deluxe',
    'Live At SoFi Stadium',
    'Alternate World',
    'Avatar: The Way of Water (Original Motion Picture Soundtrack)',
]

for album in albunsJson:
    print(album.get('name'))
    tdi = {}
    if any(item in album.get('name') for item in lista):
        continue
    tdi['id'] = album.get('id')
    tdi['name'] = album.get('name')
    albuns.append(tdi)
print(albuns)

tabela = []

for market in markets:
    for album in albuns:
        tdi = {}
        data = {
        "market": market
        }

        URL = URL_SPOTIFY_BASE + "albums/" + album.get('id')
        r = requests.get(URL,headers=headers, params=data)
        print(r.text)
        tdi['name'] = album.get('name')
        print(album.get('name'))
        tdi['total_tracks'] = r.json().get('total_tracks')
        print(r.json().get('total_tracks'))
        tdi['id'] = album.get('id')
        print(album.get('id'))
        tdi['market'] = market
        print(market)
        tdi['popularity'] = r.json().get('popularity')
        print(r.json().get('popularity'))
        tabela.append(tdi)

df = pd.DataFrame(tabela)
df.to_csv("./albuns/tabelaAlbuns.csv", index=False)