"""
TODO:
разобраться с IO задачей отлова хоткеев и настроить выход из цикла уведомлений при достаточном ознакомлении с переводом
    1)после завершения процесса уничтожать уведомление
        1.1 наверное наследоваться от класса ToastNotifier...
    2)добавить в cancel функцию отчет времени после которого возвращается False чтобы выйти из корутины
    или получше подумать над логикой...
"""

import pdfkit
from win10toast import ToastNotifier
import asyncio
from modules.Wrapper import wrapper
import pyperclip
from modules.Wrapper import wrapper
import concurrent.futures
import keyboard
import multiprocessing
import time
cfg = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

tn = ToastNotifier()


def notify_spammer(synonyms, meanings, word):
    if len(synonyms) == 0:
        for i in range(3):
            try:
                tn.show_toast(title=word, msg=meanings[i], duration=7)
            except IndexError:
                break
    else:
        title = ''
        msg = ''
        for synonym in synonyms:
            title += synonym + ' '
        for i in range(3):
            try:
                msg += meanings[i] + '\n'
            except IndexError:
                break
        tn.show_toast(title=title, msg=msg, duration=15)


def notify_killer():
    while True:
        if keyboard.is_pressed('Ctrl + Z'):
            break
        time.sleep(0.2)
    return True


async def notifier(synonyms, meanings, word):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        canceler = executor.submit(notify_killer)
        showing_func = multiprocessing.Process(target=notify_spammer, args=(synonyms, meanings, word))
        showing_func.start()
        print(canceler.result())
        if canceler.result():
            print('yep im switching')
            showing_func.terminate()
            showing_func.kill()



