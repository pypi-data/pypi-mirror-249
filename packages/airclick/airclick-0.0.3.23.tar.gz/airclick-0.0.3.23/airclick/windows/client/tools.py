import os.path
import sys
import time
import webbrowser
from PyQt5.QtWidgets import QPushButton
from airclick.windows import screen


def tools_open():
    webbrowser.open("http://127.0.0.1:8080")


def tool_capture_save() -> str:
    # pass
    img = screen.capture()

    current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # img.show()
    filename = os.path.join(current_dir,"assets/tools/capture/" + str(int(time.time())) + ".png")
    print(filename)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    return filename
    # img.save("./assets/tools/capture/"+time.time()+".png")


class ToolButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.arg = {}
