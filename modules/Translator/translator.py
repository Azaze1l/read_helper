import asyncio
import requests
from bs4 import BeautifulSoup
from modules.OutputController import output_controller

URL = 'https://dictionary.cambridge.org/dictionary/english/'
RUS_URL = 'https://dictionary.cambridge.org/ru/словарь/англо-русский/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.104 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}


async def translate(word):
    print(word)
    html = requests.get(URL + word, headers=HEADERS).text
    html_rus = requests.get(RUS_URL + word, headers=HEADERS).text
    soup_eng = BeautifulSoup(html, 'html.parser')
    soup_rus = BeautifulSoup(html_rus, 'html.parser')
    synonyms = [i.text for i in soup_rus.find_all('span', class_='sense-title dsense-title')]
    meanings = [i.text for i in soup_eng.find_all('div', class_='def ddef_d db')]
    print(synonyms)
    print(meanings)
    await output_controller.notifier(synonyms, meanings, word)
    await asyncio.sleep(0.1)
    pass
