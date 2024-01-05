import json
import os.path
import subprocess
import threading
import time

import pyautogui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QEnterEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QFileDialog, QDialog, QHBoxLayout, QLabel, QPushButton
from PyQt5.uic import loadUiType, loadUi
import sys

from PyQt5.uic.properties import QtCore

from airclick.windows.client import tools
import webbrowser
import configparser

# Load the UI file
current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# current_dir = os.path.dirname(__file__)
ui_bar_path = os.path.join(current_dir,"assets\pyui/bar.ui")
ui_step_path = "assets/pyui/step.ui"
ui_workspace_path = "assets/pyui/workspace.ui"
ui_pycharm_path = "assets/pyui/pycharminstall.ui"
ui_pyinstaller_path = os.path.join(current_dir,"assets/pyui/pyinstall.ui")
ui_home_path = "assets/pyui/home.ui"
ui_log_path = "assets/pyui/log.ui"
ui_app_item_path = "assets/pyui/item_app.ui"

py_388_path = "assets/data/python-3.8.8.exe"

py_work_config = "assets/tools/config.init"


# ui_img_bar = [os.path.join(current_dir,"assets/img/ico_run.png"),os.path.join(current_dir,"assets/img/ico_stop.png")]


class AirIcon(QIcon):
    def __init__(self, name: str):
        path = os.path.join(current_dir, "assets/img", name)
        super().__init__(path)

class BarWindow(QFrame):
    _instance = None
    log_window = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        super().__init__()
        self.is_dragging = False
        loadUi(ui_bar_path, self)
        try:
            self.home_window = HomeWindow()
        except Exception as e:
            print(str(e))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 悬浮在最顶部
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        self.capture.clicked.connect(self.btn_capture)
        self.tools.clicked.connect(tools.tools_open)
        BarWindow.log_window = LogWindow()
        self.logs.clicked.connect(self.btn_logs)
        self.app.clicked.connect(self.btn_home)

        self.ico.mousePressEvent = self.ico_down_event
        self.ico.mouseMoveEvent = self.ico_move_event
        self.ico.mouseReleaseEvent = self.ico_up_event
        self.menulabels = [self.label_capture, self.label_tools, self.label_logs, self.label_app]
        self.menubuttons = [self.capture, self.tools, self.logs, self.app]
        self.move_thread = None

        # self.run.clicked.connect()

        self.label_cap_num.setVisible(False)
        self.capture_context_num = 0

        self.auto_close_menu_time = 5
        self.start_auto_move_side_logic()

        self.run_satue = [AirIcon("ico_run.png"), AirIcon("ico_stop.png")]

        w, h = pyautogui.size()
        self.move(w - 160, h / 2 - 170)

        self.enterEvent(None)

    def enterEvent(self, event):
        self.__show_menu()
        self.label_capture.parentWidget().setStyleSheet("background-color: #90000000;border-radius:10px;")
        # self.label_capture.parentWidget().setStyleSheet("QLabel{color:white;background:#90FFFFFF; border-radius:10px;padding:5px}")

    def leaveEvent(self, event):
        self.__hide_menu()
        self.label_capture.parentWidget().setStyleSheet("background-color: #00000000")
        # self.__auto_move_side()

    def set_run_statue(self, statue: bool, num: int):
        print('?statue')
        pass

    def ico_down_event(self, event):
        if event.button() == Qt.LeftButton:
            self.ico_down_pos = QCursor.pos()
            self.offset = self.ico.pos() + event.pos()
            self.is_dragging = True

    def ico_move_event(self, event):
        if self.is_dragging:
            mouse_pos = QCursor.pos()
            self.move(mouse_pos.x() - self.offset.x(), mouse_pos.y() - self.offset.y())
            # new_pos = event.pos() - self.offset
            # self.move(new_pos)
            # self.offset = event.pos() - self.frameGeometry().topLeft()
            # print(event)

    def ico_up_event(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            temp_pos = QCursor.pos() - self.ico_down_pos
            if abs(temp_pos.x()) < 5 and abs(temp_pos.y()) < 5:
                self.start_auto_move_side_logic()

    def start_auto_move_side_logic(self):
        self.auto_close_menu_time = 5
        self.__show_menu()

    def __auto_move_side(self):
        pass

    def __hide_menu(self):
        for l in self.menulabels:
            l.setVisible(False)

        self.label_cap_num.setVisible(False)
        self.capture_context_num = 0

        for b in self.menubuttons:
            b.setVisible(False)

    def __show_menu(self):
        for l in self.menulabels:
            l.setVisible(True)

        for b in self.menubuttons:
            b.setVisible(True)

    def btn_home(self):
        try:
            self.home_window.show()
            self.home_window.setWindowState(Qt.WindowActive)
        except Exception as e:
            print(str(e))

    def btn_logs(self):
        try:
            BarWindow.log_window.show()
        except Exception as e:
            print(str(e))

    def btn_capture(self):
        # self.capture.setEnabled(False)
        self.start_auto_move_side_logic()
        tools.tool_capture_save()
        self.capture_context_num += 1
        self.label_cap_num.setText(str(self.capture_context_num))
        self.label_cap_num.setVisible(True)

        # self.capture_progress.setVisible(True)
        # def run_progress():
        #     progress_value = 0
        #
        #     while progress_value < 101:
        #         self.capture_progress.setValue(progress_value)
        #         time.sleep(0.01)
        #         progress_value += 5
        #
        #     self.capture_progress.setVisible(False)
        #
        # threading.Thread(target=run_progress).start()



class WorkSpaceWindow(QFrame):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(current_dir, ui_workspace_path), self)

        self.btn_worksapce_choose.clicked.connect(self.worksapce_choose)

        self.btn_worksaoce_submit.clicked.connect(self.submit_workspace)

    def submit_workspace(self):
        finly_workspace = self.input_worksaoce_des.text()
        work_config_file = os.path.join(current_dir, py_work_config)
        setting_dic = {}
        print(finly_workspace)

    def worksapce_choose(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        if file_dialog.exec_() == QFileDialog.Accepted:
            select_folder = file_dialog.selectedFiles()[0]
            self.input_worksaoce_des.setText(select_folder)
            self.btn_worksaoce_submit.setEnabled(True)
            print(select_folder)
            if set_workspace(select_folder):
                self.close()





class HomeWindow(QFrame):
    _instance = None
    log_window = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        super().__init__()
        loadUi(os.path.join(current_dir, ui_home_path), self)
        self.work_dir = ""
        self.app_list = []
        self.win_workspace = WorkSpaceWindow()
        self.setting_work.clicked.connect(self.fun_setting_work)
        self.setting_python.clicked.connect(self.fun_setting_python)
        self.label_work.setText(check_workspace()[1])
        self.label_py.setText(sys.executable)

        self.run_satue = [AirIcon("ico_run.png"), AirIcon("ico_stop.png")]

        self.worker = {}

    def on_run_statue(self, statue: bool):
        print(statue)
        self.addData()

        run_works = 0

        for work in self.worker:
            if self.worker[work].isRunning():
                run_works += 1

        if run_works > 0:
            BarWindow.get_instance().set_run_statue(True, run_works)
        else:
            BarWindow.get_instance().set_run_statue(False, run_works)

    def on_log_info(self, text):
        BarWindow.log_window.add_log(text)

    def on_log_error(self, text):
        BarWindow.log_window.add_log(text)

    def fun_setting_work(self):
        self.win_workspace.show()

    def fun_setting_python(self):
        self.win_pyinstall.show()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.addData()

    def addData(self):
        # 加载一下
        # self.scrool_apps_contain.r

        while self.scrool_apps_contain.rowCount() > 0:
            self.scrool_apps_contain.takeRow(0)

        workSpace, self.work_dir = check_workspace()
        self.app_list = []
        # scrool_apps_contain
        for filename in os.listdir(self.work_dir):
            file_item = os.path.join(self.work_dir, filename)
            if os.path.isdir(file_item):
                self.scrool_apps_contain.addRow(self.create_item(file_item))
                # pass
                # self.create_item(file_item)

        # self.

    def create_item(self, file: str):

        app_name = os.path.basename(file)

        def tool_click(run_btn):
            print(run_btn)
            if app_name in self.worker:
                runner = self.worker[app_name]
                if runner.isRunning():
                    runner.stop()
                else:
                    runner.start()
            else:
                runner = RunThread(file)
                runner.run_statue.connect(self.on_run_statue)
                runner.log_info.connect(self.on_log_info)
                runner.log_error.connect(self.on_log_error)
                self.worker[runner.name] = runner
                runner.start()

        frame = loadUi(os.path.join(current_dir, ui_app_item_path), None)
        frame.label.setText(app_name)

        try:
            if app_name in self.worker:
                if self.worker[app_name].isRunning():
                    frame.run_btn.setIcon(self.run_satue[1])
                else:
                    frame.run_btn.setIcon(self.run_satue[0])
            else:
                frame.run_btn.setIcon(self.run_satue[0])
        except Exception as e:
            print(str(e))

        frame.run_btn.clicked.connect(lambda checked: tool_click(frame.run_btn))
        return frame


class LogWindow(QFrame):
    max_lines = 100

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(os.path.join(current_dir, ui_log_path), self)

    def add_log(self, msg: str):
        if self.form_log.rowCount() >= 10:
            self.form_log.removeRow(0)

        l_t = QLabel(self)
        l_t.setText("时间")
        l_msg = QLabel(self)
        l_msg.setText(msg)
        l_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.form_log.addRow(l_t, l_msg)
        vbar = self.scrollArea.verticalScrollBar()
        vbar.setValue(vbar.maximum())


class RunThread(QThread):
    log_info = pyqtSignal(str)
    log_error = pyqtSignal(str)
    run_statue = pyqtSignal(bool)

    def __init__(self, path_file: str):
        super().__init__()
        self.proc = None
        self.path = path_file
        self.name = os.path.basename(self.path)

    def pause(self):
        if self.proc:
            self.proc.suspend()

    def stop(self):
        if self.proc:
            self.proc.terminate()

    def run(self) -> None:
        self.run_statue.emit(True)
        main_file = os.path.join(self.path, 'main.py')
        main_file = main_file.replace('\\', '/')
        if os.path.exists(main_file):
            try:
                print(main_file)
                with subprocess.Popen(['python', main_file], stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as self.proc:
                    for line in self.proc.stdout:
                        print("?-" + line.decode('utf-8').strip())  # 打印标准输出的一行
                        self.log_info.emit(line.decode('utf-8').strip())

                    for line in self.proc.stderr:
                        # log_win.add_log(line.decode('utf-8').strip())
                        print(line.decode('utf-8').strip())  # 打印标准错误的一行
                        self.log_error.emit(line.decode('utf-8').strip())
            except Exception as e:
                print(str(e))

        self.name = None
        self.run_statue.emit(False)


def enter():
    try:
        app = QApplication(sys.argv)

        step3, msg = check_workspace()

        # 检测完毕后，再打开悬浮窗口
        if step3:

            bar_window = BarWindow()
            # bar_window = FloatWindow()
            bar_window.show()
        else:
            workspace_win = WorkSpaceWindow()
            workspace_win.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))



def choose_andsetting_env(intput_view, callback):
    def child_run():
        try:
            res = subprocess.run([select_file, "--version"])
            if res:
                select_dir = os.path.dirname(select_file)
                select_dir = select_dir.replace('/', '\\')
                # 设置环境变量
                # Machine 是系统，User 是用户
                subprocess.run(['powershell',
                                f'[System.Environment]::SetEnvironmentVariable("Path","{select_dir}" +";" + $env:Path, [System.EnvironmentVariableTarget]::Machine)'])
                subprocess.run(['echo', '%PATH%'], shell=True)

                # 设置当前进程环境变量
                current_path = os.environ['PATH']
                os.environ['PATH'] = select_dir + ";" + current_path
                callback(True, "")
        except Exception as e:
            callback(False, str(e))

    file_dialog = QFileDialog()
    if file_dialog.exec_() == QDialog.Accepted:
        select_file = file_dialog.selectedFiles()[0]
        intput_view.setText(select_file)
        threading.Thread(target=child_run).start()


def set_workspace(path: str):
    try:
        work_config_file = os.path.join(current_dir, py_work_config)
        config = configparser.ConfigParser()
        config['workspace'] = {'path': path}
        with open(work_config_file, 'w') as configfile:
            config.write(configfile)

        return True
    except Exception as e:
        print(str(e))
        return False


def check_workspace():
    try:
        work_config_file = os.path.join(current_dir, py_work_config)
        config = configparser.ConfigParser()
        config.read(work_config_file)
        if config.has_section('workspace') and config.has_option('workspace', 'path'):
            print(config['workspace']['path'])
            return True, config['workspace']['path']
    except Exception as e:
        print("e:" + str(e))
        return False, str(e)

    return False, ""


def get_workspace_list():
    workSpace, work_dir = check_workspace()
    app_list = []
    # scrool_apps_contain
    if workSpace:
        for filename in os.listdir(work_dir):
            file_item = os.path.join(work_dir, filename)
            if os.path.isdir(file_item):
                app_list.append(file_item)

    return app_list
