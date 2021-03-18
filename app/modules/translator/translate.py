import requests
from logger import logger
from bs4 import BeautifulSoup
from modules.wrapper import hotkey_catcher
from modules.output_controller import notify_controller
from modules.parser import parse_pronunciation
from modules.output_controller import pronunciation_player
import multiprocessing
from settings import UK_PRONUNCIATION, US_PRONUNCIATION


URL = 'https://dictionary.cambridge.org/dictionary/english/'
RUS_URL = 'https://dictionary.cambridge.org/ru/словарь/англо-русский/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.104 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}


async def find_synonyms_and_definitions(word):
    logger.info(f'Переводится слово: {word}')
    html = requests.get(URL + word, headers=HEADERS).text
    html_rus = requests.get(RUS_URL + word, headers=HEADERS).text
    soup_eng = BeautifulSoup(html, 'html.parser')
    soup_rus = BeautifulSoup(html_rus, 'html.parser')
    sections = soup_eng.find_all('div', class_='pr entry-body__el')
    word_classes = []
    meanings = []
    for section in sections:
        try:
            word_class = section.find('div', class_='posgram dpos-g hdib lmr-5').find('span').text
            meanings_on_section = [i.text.replace(': ', '') for i in section.find_all('div', class_='def ddef_d db')]
            word_classes.append(word_class)
            meanings.append(meanings_on_section)
        except AttributeError:
            logger.info('Это слово не найдено в словаре')
            await hotkey_catcher.catch_searching_hotkey()
    synonyms = [i.text for i in soup_rus.find_all('span', class_='sense-title dsense-title')]
    pronunciations = []
    try:
        uk_pr, us_pr = parse_pronunciation.parse(html)
        if UK_PRONUNCIATION:
            pronunciations.append(uk_pr)
        if US_PRONUNCIATION:
            pronunciations.append(us_pr)
        pronunciation_proc = multiprocessing.Process(target=pronunciation_player.play, args=(pronunciations,))
        pronunciation_proc.start()
    except Exception:
        pass
    await notify_controller.notifier(synonyms, meanings, word_classes, word)

