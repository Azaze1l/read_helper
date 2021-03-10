import keyboard
import pyperclip
import time
import asyncio
from loop import loop
from modules.Translator import translator


async def hotkey_catcher():
    while True:
        word = pyperclip.paste()
        if keyboard.is_pressed('Ctrl + C + S'):
            await translator.translate(word)
        await asyncio.sleep(0.1)

