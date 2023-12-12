import requests
from bs4 import BeautifulSoup
import pandas as pd

URL_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"

data = {
    "grant_type": "client_credentials",
    "client_id": "8aa217ba6aa641ba9999fc9383cfe260",
    "client_secret": "0e8f0ab115e24fdba239455799da14f1"
}

response = requests.post(URL_SPOTIFY_TOKEN, data=data)

token = response.json().get('access_token')

print(token)
