from loop import loop
from modules import *
from logger import logger


if __name__ == '__main__':
    logger.info('Приложение запущено')
    task = loop.create_task(wrapper.hotkey_catcher.catch_searching_hotkey())
    loop.run_until_complete(task)
