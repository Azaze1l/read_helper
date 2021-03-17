from playsound import playsound
import time
from logger import logger


def play(urls: dict):
    logger.info('Озвучивается слово')
    for url in urls:
        playsound(url)
        time.sleep(1)
