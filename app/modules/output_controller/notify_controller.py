"""
TODO:
разобраться с IO задачей отлова хоткеев и настроить выход из цикла уведомлений при достаточном ознакомлении с переводом
    1)после завершения процесса уничтожать уведомление
        1.1 наверное наследоваться от класса ToastNotifier...

"""

import pdfkit
from win10toast import ToastNotifier
import keyboard
import multiprocessing
import time


cfg = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

tn = ToastNotifier()


def notify_spammer(synonyms, meanings, word):
    if len(synonyms) == 0 and len(meanings) != 0:
        for meaning in meanings:
            tn.show_toast(title=word, msg=meaning, duration=7)
    elif len(synonyms) == len(meanings) == 0:
        tn.show_toast(title='Oops', msg='Ничего не найдено')
    else:
        title = '|'
        for synonym in synonyms:
            title += synonym + '|'
        for i in range(len(meanings)):
            tn.show_toast(title=title, msg=meanings[i], duration=7)


def notify_killer():
    while True:
        if keyboard.is_pressed('Ctrl + Z'):
            break
        time.sleep(0.1)


async def notifier(synonyms, meanings, word):
    showing_func = multiprocessing.Process(target=notify_spammer, args=(synonyms, meanings, word))
    showing_func.start()
    canceler_proc = multiprocessing.Process(target=notify_killer)
    canceler_proc.start()
    while showing_func.is_alive():
        if not canceler_proc.is_alive():
            showing_func.kill()
            break
        time.sleep(0.1)
    print('yep im switching')

