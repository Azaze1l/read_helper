"""
TODO:
разобраться с IO задачей отлова хоткеев и настроить выход из цикла уведомлений при достаточном ознакомлении с переводом
"""

import pdfkit
from win10toast import ToastNotifier
import asyncio
from modules.Wrapper import wrapper
import pyperclip
import keyboard

cfg = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')


async def notifier(synonyms, meanings, word):
    tn = ToastNotifier()
    if len(synonyms) == 0:
        for i in range(3):
            if keyboard.is_pressed('Ctrl + C + X'):
                print('switched')
                await wrapper.hotkey_catcher()
                break
            else:
                try:

                    tn.show_toast(title=pyperclip.paste(), msg=meanings[i], duration=7)
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
        tn.show_toast(title=title, msg=msg, duration=20)

