import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse


url = 'https://www.letras.mus.br/the-weeknd/mais_acessadas.html'
response = requests.get(url)

lista = []

URL_SPOTIFY_BASE = "https://api.spotify.com/v1/"

URL_SPOTIFY_MARKETS = URL_SPOTIFY_BASE + "markets"

URL_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"

URL_TRACKS = URL_SPOTIFY_BASE + 'artists/1Xyo4u8uXC1ZmMpatF05PJ/top-tracks'

data = {
    "grant_type": "client_credentials",
    "client_id": "8aa217ba6aa641ba9999fc9383cfe260",
    "client_secret": "0e8f0ab115e24fdba239455799da14f1"
}

responseToken = requests.post(URL_SPOTIFY_TOKEN, data=data)

token = responseToken.json().get('access_token')

headers = {
    'Authorization': 'Bearer {}'.format(token)
}


soup = BeautifulSoup(response.text, 'html.parser')
results = soup.find_all('li', class_='songList-table-row --song isVisible')

def remove(original_string):
    index = original_string.find("(")
    if index != -1:
        result_string = original_string[:index]
        return result_string
    else:
        return original_string
    

for result in results:
    tdi = {}
    letra = ''
         
    link = result.find('a')
    span_element = result.find('span')


    urlMusica = 'https://www.letras.mus.br' + link['href']
    responseMusica = requests.get(urlMusica)
    soup = BeautifulSoup(responseMusica.text, 'html.parser')
    resultsMusica = soup.find_all('div', class_='lyric-original')

    for element in resultsMusica:
        paragraphs = element.find_all('p')
        for paragraph in paragraphs:
            p_with_space = paragraph.get_text(separator=' ') + ' '
            letra += p_with_space
    
    tdi['href'] = link['href']
    print(link['href'])

    tdi['letra'] = letra
    print(letra)


    nome = span_element.get_text()

    result = remove(nome)


    tdi['nome'] = result

    a = result

    result = a.replace("'", "").replace("’", "")
    print(result)

    dataQuery={
        'q': "track:" + result + "artist:The%20Weeknd",
        'type': 'track'
    }

    URL_TRACK = URL_SPOTIFY_BASE + "search?q=track:" + result + "%20" + "artist:The%20Weeknd&type=track"
    try:
        responseTrack = requests.get(URL_TRACK, headers=headers)
        print(responseTrack.url)
        item = responseTrack.json().get('tracks').get('items')
        albumNome = item[0].get('album').get('name')
        trackID = item[0].get('id')
        tdi['album'] = albumNome
        print(albumNome)
        tdi['trackID'] = trackID
        print(trackID)
        try:
            URL_FEATURES = URL_SPOTIFY_BASE + "audio-features/" + trackID
            responseFeatures = requests.get(URL_FEATURES, headers=headers)
            json = responseFeatures.json()
            tdi['acousticness'] = json.get('acousticness')
            print(tdi['acousticness'])
            tdi['danceability'] = json.get('danceability')
            print(tdi['danceability'])
            tdi['duration'] = json.get('duration_ms')
            print(tdi['duration'])
            tdi['energy'] = json.get('energy')
            print(tdi['energy'])
            tdi['loudness'] = json.get('loudness')
            print(tdi['loudness'])
            tdi['valence'] = json.get('valence')
            print(tdi['valence'])
        except:
            tdi['acousticness'] = None
            tdi['danceability'] = None
            tdi['duration'] = None
            tdi['energy'] = None
            tdi['loudness'] = None
            tdi['valence'] = None

    except:
        tdi['album'] = None
        tdi['trackID'] = None
    

    lista.append(tdi)

df = pd.DataFrame(lista)
df['contagem_XO'] = df['letra'].str.count('XO')
df.dropna(subset=['trackID'])

df.to_csv("./letras/tabelaTheWeeknd.csv", index=False)

