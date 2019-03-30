import os
import sys
import time
import random
import configparser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qtwidgets import *
from PyQt5.QtMultimedia import *


class musicplayer(QWidget):

    def __init__(self):
        super().__init__()
        self.__initialization()

    def __initialization(self):
        self.setWindowTitle('MusicPlayer V0.1')
        self.setWindowIcon()  # TODO: set Icon
        self.song_list = []
        self.song_formats = ['mp3', 'm4a', 'wav', 'flac']
        self.configfile = 'configuration.ini'
        self.player = Qmediaplayer()
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.cur_song = ''
        self.switch = False
        self.pause = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mod = musicplayer()
    mod.show()
    sys.exit(app.exec_)
