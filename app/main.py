from app.loop import loop
from modules import *
if __name__ == '__main__':
    task = loop.create_task(wrapper.hotkey_catcher.catch_searching_hotkey())
    loop.run_until_complete(task)
