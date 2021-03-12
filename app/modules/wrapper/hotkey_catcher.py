import keyboard
import pyperclip
import asyncio
import settings
from modules.translator import translate


async def catch_searching_hotkey():
    while True:
        word = pyperclip.paste()
        if keyboard.is_pressed(settings.SEARCHING_HOTKEY):
            await translate.find_synonyms_and_definitions(word)
        await asyncio.sleep(0.1)

