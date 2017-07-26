#! /usr/bin/python3
import os
import logging

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(PATH, 'log')
BASE_URL = 'http://210.77.16.21/eportal/InterFace.do?method='
TIME_OUT = 5
EXCEPTIONS = (
    AttributeError, IOError, NotImplementedError,
    TimeoutError, IndexError, ConnectionError, FileExistsError,
    ValueError, TypeError, RuntimeError, ConnectionAbortedError,
    IndentationError, InterruptedError, KeyError, StopIteration,
)
POSTDATA_LOGIN = {
    'operatorPwd': '',
    'password': 'ucas',
    'queryString': 'wlanuserip%253D0bc386d9e643d188b011a0d00c9b5c40%2526wlanacname%253D'
    + '5fcbc245a7ffdfa4%2526ssid%253D%2526nasip%253D2c0716b583c8ac3cbd7567a84cfde5a8%'
    + '2526mac%253D53ba540bde596b811a6d5617a86fa028%2526t%253Dwireless-v2%'
    + '2526url%253D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30',
    'service': '',
    'userId': '',
    'validcode': ''
}
POSTDATA = {'userIndex': ''}
DATA = {
    'userId': '',
    'result': '',
    'userIndex': '',
    'maxFlow': '',
    'userName': ''
}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    + '(KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
}


def get_logger(name, log_path):
    '返回一个logger, name是名字'
    formatter = logging.Formatter(
        '[%(asctime)s] "%(levelname)s"  %(message)s',
        '%d/%b/%Y %H:%M:%S'
    )
    handle = logging.FileHandler(log_path)
    handle.setLevel(logging.INFO)
    handle.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handle)
    return logger


def clear(diction, item=''):
    '将字典中每个项都赋值成item, 默认为空'
    for key, _ in diction.items():
        diction[key] = item


def store_data(file_name, data, endwith='\n'):
    '存储到文件, 自动换行'
    write_data = [each + endwith for each in data]
    with open(file_name, 'w') as file:
        file.writelines(write_data)


class Status(object):
    GUI = False
    MAIN = None
    UPDATE = None
    UPDATE_DLG = None

    _LOGIN = False
    _RUN = False
    _USER = ''
    _FLOW = ''
    _UPDATE_ALL = 0
    _UPDATE_NOW = 0

    @property
    def LOGIN(self):
        return self._LOGIN

    @property
    def RUN(self):
        return self._RUN

    @property
    def USER(self):
        return self._USER

    @property
    def FLOW(self):
        return self._FLOW

    @property
    def UPDATE_ALL(self):
        return self._UPDATE_ALL

    @property
    def UPDATE_NOW(self):
        return self._UPDATE_NOW

    @LOGIN.setter
    def LOGIN(self, value):
        self._LOGIN = value
        if self.GUI and self.MAIN:
            self.MAIN.info_update()

    @RUN.setter
    def RUN(self, value):
        self._RUN = value
        if self.GUI and self.MAIN:
            self.MAIN.info_update()

    @USER.setter
    def USER(self, value):
        self._USER = value
        if self.GUI and self.MAIN:
            self.MAIN.info_update()

    @FLOW.setter
    def FLOW(self, value):
        self._FLOW = value
        if self.GUI and self.MAIN:
            self.MAIN.info_update()

    @UPDATE_ALL.setter
    def UPDATE_ALL(self, value):
        self._UPDATE_ALL = value
        if self.UPDATE:
            self.UPDATE.all.setText(str(self._UPDATE_ALL))

    @UPDATE_NOW.setter
    def UPDATE_NOW(self, value):
        self._UPDATE_NOW = value
        if self.UPDATE:
            self.UPDATE.now.setText(str(self._UPDATE_NOW))



STATUS = Status()
LOG = get_logger('auto_login', LOG_PATH)
