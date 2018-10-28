import ctypes
import datetime
from time import sleep

from Utils import string_resizer

SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event

is_mouse_clicked = False


class LeftClicker:
    def __init__(self, clickmemory):
        self.clickmemory = clickmemory
        self.isLeftDown = False
        self.isLeftUp = True

    def left_click(self, delay_before=0, delay_between=0, testing=False):
        global is_mouse_clicked

        if testing:
            return False

        if not is_mouse_clicked:
            is_mouse_clicked = True
            sleep(delay_before)
            downtime = datetime.datetime.now().time()
            mouse_event(2, 0, 0, 0, 0)

            sleep(delay_between)
            mouse_event(4, 0, 0, 0, 0)
            print("Click:", string_resizer(str(self.clickmemory.totalClick + 1), 7),
                  downtime, " - ", datetime.datetime.now().time(),
                  "\t waited/Lasted", delay_before, " - ", delay_between)
            is_mouse_clicked = False
        else:
            print("Mouse is already pressed. Stopping Thread...")
            return True

        return False
