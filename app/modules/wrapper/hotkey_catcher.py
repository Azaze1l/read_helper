import keyboard
import pyperclip
import asyncio
from app.modules.translator import translate


async def catch_searching_hotkey():
    while True:
        word = pyperclip.paste()
        if keyboard.is_pressed('Ctrl + C + S'):
            await translate.find_synonyms_and_definitions(word)
        await asyncio.sleep(0.1)

