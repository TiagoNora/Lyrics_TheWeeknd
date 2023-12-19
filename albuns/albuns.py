import requests
import json
import pandas as pd

URL_SPOTIFY_BASE = "https://api.spotify.com/v1/"

URL_SPOTIFY_MARKETS = URL_SPOTIFY_BASE + "markets"

URL_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"

URL_TRACKS = URL_SPOTIFY_BASE + 'artists/1Xyo4u8uXC1ZmMpatF05PJ/top-tracks'

URL_ALBUNS = URL_SPOTIFY_BASE + 'artists/1Xyo4u8uXC1ZmMpatF05PJ/albums'

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



dataAlbum = {
    "include_groups": "album",
    "market": "PT",
    "limit": "50",
    "offset": "0"
}

responseAlbuns = requests.get(URL_ALBUNS,headers=headers, params=dataAlbum)

albunsJson = responseAlbuns.json().get('items')

albuns = []

for album in albunsJson:
    tdi = {}
    if "Deluxe" in album.get('name'):
        continue
    tdi['id'] = album.get('id')
    tdi['name'] = album.get('name')
    print(album.get('name'))
    albuns.append(tdi)

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
