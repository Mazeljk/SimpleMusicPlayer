#!/usr/bin/python3
# -*- coding: utf-8- -*-

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
        self.setWindowIcon(QIcon())  # TODO: set Icon
        self.song_list = []
        self.song_formats = ['mp3', 'm4a', 'wav', 'flac']
        self.configfile = 'configuration.ini'
        self.player = Qmediaplayer()
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.cur_song = ''
        self.switch = False
        self.pause = False

        # playing time
        self.lable1 = QLabel('00:00')
        self.label1.setStyle(QStyleFactory.create('Fusion'))
        self.lable2 = QLable('00:00')
        self.lable2.setStyle(QStyleFactory.create('Fusion'))

        # slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.sliderMoved[int].connect(
            lambda: self.player.setPosition(self.slider.value()))
        self.slider.setStyle(QStyleFactory.create('Fusion'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = musicplayer()
    GUI.show()
    sys.exit(app.exec_)
