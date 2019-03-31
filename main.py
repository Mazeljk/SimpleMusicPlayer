#!/usr/bin/python3
# -*- coding: utf-8- -*-

import os
import sys
import time
import random
import configparser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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
        self.player = QMediaPlayer()
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.cur_song = ''
        self.switch = False
        self.pause = False

        # playing time
        self.label1 = QLabel('00:00')
        self.label1.setStyle(QStyleFactory.create('Fusion'))
        self.label2 = QLabel('00:00')
        self.label2.setStyle(QStyleFactory.create('Fusion'))

        # progress bar
        self.slider = QSlider(Qt.Horizontal, self)
        # TODO
        # self.slider.sliderMoved[int].connect(
        #    lambda: self.player.setPosition(self.slider.value()))
        self.slider.setStyle(QStyleFactory.create('Fusion'))

        # play button
        self.pbtn = QPushButton('Play', self)
        # TODO
        # self.pbtn.clicked.connect(self.playMusic)
        self.pbtn.setStyle(QStyleFactory.create('Fusion'))

        # preview button
        self.prebtn = QPushButton('Preview', self)
        # TODO
        # self.prebtn.clicked.connect(self.previewMusic)
        self.prebtn.setStyle(QStyleFactory.create('Fusion'))

        # next button
        self.nbtn = QPushButton('Next', self)
        # TODO
        # self.nbtn.clicked.connect(self.nextMusic)
        self.nbtn.setStyle(QStyleFactory.create('Fusion'))

        # open button
        self.obtn = QPushButton('Open file/folder..', self)
        # TODO
        # self.obtn.clicked.connect(self.opendir)
        self.obtn.setStyle(QStyleFactory.create('Fusion'))

        # display button
        self.displaybtn = QPushButton('Display list', self)
        # TODO
        # self.displaybtn.itemDoubleClicked.connect(self.doubleClicked)
        self.displaybtn.setStyle(QStyleFactory.create('Fusion'))

        # play mode
        self.play_mode = QComboBox()
        self.play_mode.addItem('Order')
        self.play_mode.addItem('Repeat once')
        self.play_mode.addItem('Shuffle')
        self.play_mode.setStyle(QStyleFactory.create('Fusion'))

        # timer
        self.timer = QTimer(self)
        self.timer.start(1000)
        # TODO
        # self.timer.timeout.connect(self.playByMode)

        # layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.displaybtn, 0, 0, 5, 10)
        self.grid.addWidget(self.label1, 0, 11, 1, 1)
        self.grid.addWidget(self.slider, 0, 12, 1, 1)
        self.grid.addWidget(self.label2, 0, 13, 1, 1)
        self.grid.addWidget(self.pbtn, 0, 14, 1, 1)
        self.grid.addWidget(self.nbtn, 1, 11, 1, 2)
        self.grid.addWidget(self.prebtn, 2, 11, 1, 2)
        self.grid.addWidget(self.play_mode, 3, 11, 1, 2)
        self.grid.addWidget(self.obtn, 4, 11, 1, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = musicplayer()
    GUI.show()
    sys.exit(app.exec_)
