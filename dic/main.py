import sys
import requests
from bs4 import BeautifulSoup

word = sys.argv[-1]
url = "https://ejje.weblio.jp/content/{}".format(word)

r = requests.get(url)
data = BeautifulSoup(r.text, 'html.parser')

for meta in data.find_all('meta'):
    if meta.get('name') == 'twitter:description':
        print(meta.get('content'))