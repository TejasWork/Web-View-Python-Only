import sys
import os
import signal

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from flask import *
from threading import Thread
import json
import logging

server_log = logging.getLogger('werkzeug')
server_log.setLevel(logging.ERROR)

def post_json(_json_: dict) -> Response:
    return make_response(jsonify(_json_, 200))

def get_json() -> dict:
    return json.loads(request.get_data().decode('utf-8'))

def parse_local_qurl(path: str) -> QUrl:
    if path[0:4] == 'http':
        return QUrl(path)
    elif path[0:2] == './' or path[0:2] == '.\\':
        path = path[2:]
    else:
        return QUrl(path.replace('\\', '/'))
    return QUrl(f'{os.getcwd()}\\{path}'.replace('\\', '/'))

class database():

    def __init__(self) -> None:
        file_string = '{}'
        if os.path.isfile('database.json'):
            file = open('database.json', 'r+')
            file_string = file.read()
            file.close()
        else:
            file = open('database.json', 'w+')
            file.write('{}')
            file.close()
        self.__dict__ = json.loads(file_string)

    def save(self):
        file = open('database.json', 'w+')
        file.write(json.dumps(self.__dict__))
        file.close()

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

class application:
    def __init__(self, port: int) -> None:
        self.qt_application = QApplication(sys.argv)
        self.server = Flask("Web App")
        self.host = 'localhost'
        self.port = port
        self.screen = self.qt_application.primaryScreen()
        self.screen_width = self.screen.size().width()
        self.screen_height = self.screen.size().height()
    def start(self) -> int:
        Thread(target=self.server.run, args=[self.host, self.port]).start()
        return self.qt_application.exec_()

class window():
    def __init__(self, port: int = 5000):
        self.qt_window = QMainWindow()
        self.qt_web_engine = QWebEngineView()
        self.qt_web_engine.setZoomFactor(1.27)
        self.qt_web_engine.setContextMenuPolicy(Qt.NoContextMenu)
        self.qt_window.setCentralWidget(self.qt_web_engine)
        self.port = port
        self.host = 'localhost'
    def show_maximized(self):
        self.qt_window.showMaximized()
    def set_route(self, route_path: str):
        self.qt_web_engine.setUrl(QUrl(f'http://{self.host}:{self.port}{route_path}'))
    def set_html(self, website_or_html_path: str):
        self.qt_web_engine.setUrl(parse_local_qurl(website_or_html_path))
    def set_zoom(self, zoom_value: float):
        self.qt_web_engine.setZoomFactor(zoom_value)
    def get_zoom(self) -> float:
        return self.qt_web_engine.zoomFactor()
    def set_title(self, title: str):
        self.qt_window.setWindowTitle(title)
    def get_title(self) -> str:
        return self.qt_window.windowTitle()
    def set_icon(self, icon_path: str):
        self.qt_window.setWindowIcon(QIcon(icon_path))
    def set_x(self, x: int):
        self.qt_window.move(x, self.qt_window.y())
    def get_x(self) -> int:
        return self.qt_window.x()
    def set_y(self, y: int):
        self.qt_window.move(self.qt_window.x(), y)
    def get_y(self) -> int:
        self.qt_window.y()
    def lock_width(self):
        self.qt_window.setFixedWidth(self.qt_window.width())
    def set_width(self, width: int):
        self.qt_window.resize(width, self.qt_window.height())
    def get_width(self) -> int:
        return self.qt_window.width()
    def set_maximum_width(self, maximum_width: int):
        self.qt_window.setMaximumWidth(maximum_width)
    def get_maximum_width(self) -> int:
        return self.qt_window.maximumWidth()
    def lock_height(self):
        self.qt_window.setFixedHeight(self.qt_window.height())
    def set_height(self, height: int):
        self.qt_window.resize(self.qt_window.width(), height)
    def get_height(self) -> int:
        return self.qt_window.height()
    def set_maximum_height(self, maximum_height: int):
        self.qt_window.setFixedHeight(maximum_height)
    def get_maximum_height(self) -> int:
        return self.qt_window.maximumHeight()
    def show(self):
        self.qt_window.show()

def force_quit():
    os.kill(os.getpid(), signal.SIGILL)