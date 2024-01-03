import ctypes
import sys
import pyautogui
import win32con
import win32gui
from PIL import ImageGrab, Image, ImageQt
import re

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)


class Window:

    @staticmethod
    def find(active: bool = True, title: str = None, name: str = None, hwnd: int = None):

        if hwnd:
            return Window(hwnd)

        window_list = Window.find_all(active, title, name)
        if window_list and len(window_list) > 0:
            return window_list[0]

        return None

    @staticmethod
    def find_all(active: bool = None, title: str = None, name: str = None):
        window_list = []

        def tempcall(hwnd, list):
            window_list.append(Window(hwnd, False))

        win32gui.EnumWindows(tempcall, window_list)

        f_window_list = []
        for w in window_list:

            if active is not None:
                if active != w.is_active():
                    continue

            if title is not None:
                if not w.__base_re(title, w.title):
                    continue

            if name is not None:
                if not w.__base_re(name, w.title):
                    continue

            f_window_list.append(w)

        return f_window_list

    @staticmethod
    def active():
        return Window(win32gui.GetForegroundWindow())

    @staticmethod
    def screen_size():
        return pyautogui.size()

    def __init__(self, hwnd: int, fill_children: bool = True):
        self.qapp = None
        self.children = None
        self.hwnd = hwnd
        self.title = win32gui.GetWindowText(hwnd)
        self.rect = win32gui.GetWindowRect(hwnd)
        self.name = win32gui.GetClassName(hwnd)
        # 是否最小化
        if fill_children:
            self.__fill_childs(hwnd)

    def __fill_childs(self, hwnd: int):
        self.children = []

        def node_enum(hwnd, extra):
            self.children.append(Window(hwnd))

        win32gui.EnumChildWindows(hwnd, node_enum, None)

    def __str__(self):
        return {'hwnd':self.hwnd,'title':self.title,'name':self.name,'rect':self.rect,'active':self.is_active()}.__str__()

    def to_dict(self):
        tempchilds = []

        if self.children:
            for cnode in self.children:
                tempchilds.append(cnode.to_dict())

        return {
            'hwnd': self.hwnd,
            'name': self.name,
            'title': self.title,
            'rect': self.rect,
            'children': tempchilds,
            "placement": self.placement(),
            # "is_maximized": self.is_maximized(),
            "is_active": self.is_active(),
            "has_focus": self.has_focus(),
        }

    def capture(self) -> Image:
        return pyautogui.screenshot()

    def views(self):
        pass

    def is_active(self):
        return win32gui.GetForegroundWindow() == self.hwnd

    def has_focus(self):
        return win32gui.GetFocus() == self.hwnd

    def placement(self):
        # return ctypes.windll.user32.IsIconic(self.hwnd) != 0
        return win32gui.GetWindowPlacement(self.hwnd)[0]

    def frame(self, x=None, y=None, w=None, h=None):

        if x is None:
            x = self.rect[0]

        if y is None:
            y = self.rect[1]

        if w is None:
            w = self.rect[2] - self.rect[0]

        if h is None:
            h = self.rect[3] - self.rect[1]

        win32gui.MoveWindow(self.hwnd, int(x), int(y), int(w), int(h), True)

    def mize_mini(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)

    def mize_max(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

    def mize_normal(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)

    def close(self):
        win32gui.SendMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    def __base_re(self, pattern, value):
        if not re.match(pattern, value):
            return False

        return True


class Selector:

    def __init__(self, model: int = 0, dict=None, ):
        self.find_max = -1
        self.model = model
        self.sels = []

        # 初始化json
        if dict:
            self.model = int(dict['model'])
            self.sels = dict['sels']
            self.find_max = dict['find']

    def find(self):
        self.find_max = 1

        find_res = self.exec_find()

        if find_res and len(find_res) > 0:
            return find_res[0]

        return None

    def find_all(self, num: int = sys.maxsize):
        self.find_max = -1
        return self.exec_find()

    def exec_find(self):
        window_list = []

        if self.model <= 0:
            def tempcall(hwnd, list):
                if self.model == 0:
                    window_list.append(Window(hwnd, False))
                elif self.model == -1:
                    window_list.append(Window(hwnd))

            win32gui.EnumWindows(tempcall, window_list)
        else:
            window_list.append(Window(self.model))

        return self.__check(window_list)

    def title(self, title: str):
        self.sels.append({"key": "title", "value": title})
        return self

    def name(self, name: str):
        self.sels.append({"key": "name", "value": name})
        return self

    def hwnd(self, hwnd: str):
        self.sels.append({"key": "hwnd", "value": hwnd})
        return self

    def __check(self, node_list):
        if len(self.sels) < 1:
            return node_list

        res_nodes = []
        for node in node_list:
            for sel in self.sels:
                if self.find_max > 0 and len(res_nodes) >= self.find_max:
                    return res_nodes

                key = sel['key']
                vales = sel['value']
                if key == "title":
                    if self.__base_re(vales, node.title):
                        res_nodes.append(node)

                if key == "name":
                    if self.__base_re(vales, node.name):
                        res_nodes.append(node)

                if key == "hwnd":
                    if self.__base_re(vales, node.hwnd):
                        res_nodes.append(node)

        return res_nodes


