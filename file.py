import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.letras.mus.br/the-weeknd/mais_acessadas.html'
response = requests.get(url)

lista = []

soup = BeautifulSoup(response.text, 'html.parser')
results = soup.find_all('li', class_='songList-table-row --song isVisible')

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

    tdi['nome'] = span_element.get_text()
    print(span_element.get_text())

    lista.append(tdi)

df = pd.DataFrame(lista)
df.to_csv("./versao 2/dados.csv", index=False)

