from bs4 import BeautifulSoup

URL = 'https://dictionary.cambridge.org/'


def parse(html):
    bf = BeautifulSoup(html, 'html.parser')
    pronunciations = bf.find_all('span', class_='daud')
    uk_pr = URL + pronunciations[0].find('amp-audio').find('source', type='audio/mpeg').get('src')
    us_pr = URL + pronunciations[1].find('amp-audio').find('source', type='audio/mpeg').get('src')
    return uk_pr, us_pr
