import pdfkit
from win10toast import ToastNotifier
import keyboard
import multiprocessing
import time
import settings
from logger import logger
cfg = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

tn = ToastNotifier()


def notify_spammer(synonyms, meanings, word_classes, word):
    if len(synonyms) == 0 and len(meanings) != 0:
        for i in range(len(word_classes)):
            for j in range(len(meanings[i])):
                tn.show_toast(title=word + f' ({word_classes[i]})', msg=meanings[i][j], duration=settings.TOAST_DURATION)
    elif len(synonyms) == len(meanings) == 0:
        tn.show_toast(title='Oops', msg='Ничего не найдено')
    else:
        title = f'{word}>>|'
        for synonym in synonyms:
            title += synonym + '|'
        for i in range(len(word_classes)):
            for j in range(len(meanings[i])):
                tn.show_toast(title=title, msg=f'({word_classes[i]}): ' + meanings[i][j], duration=settings.TOAST_DURATION)


def notify_killer():
    while True:
        if keyboard.is_pressed(settings.CANCELING_HOTKEY):
            break
        time.sleep(0.1)


async def notifier(synonyms, meanings, word_classes, word):
    showing_func = multiprocessing.Process(target=notify_spammer, args=(synonyms, meanings, word_classes, word))
    showing_func.start()
    canceler_proc = multiprocessing.Process(target=notify_killer)
    canceler_proc.start()
    while showing_func.is_alive():
        if not canceler_proc.is_alive():
            showing_func.kill()
            logger.info('Выполнено досрочное завершение')
            break
        time.sleep(0.1)
    logger.info('Приведены все найденные переводы')

