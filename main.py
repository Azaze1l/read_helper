import keyboard
import pyperclip

from win10toast import ToastNotifier
from loop import loop
from modules.Wrapper import wrapper


if __name__ == '__main__':
    task = loop.create_task(wrapper.hotkey_catcher())
    loop.run_until_complete(task)
