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
        self.config = 'config.ini'
        self.player = QMediaPlayer()
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.cur_playing_song = ''
        self.switch = False
        self.pause = True

        # playing time
        self.label1 = QLabel('00:00')
        self.label1.setStyle(QStyleFactory.create('macintosh'))
        self.label2 = QLabel('00:00')
        self.label2.setStyle(QStyleFactory.create('macintosh'))

        # progress bar
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.sliderMoved[int].connect(
            lambda: self.player.setPosition(self.slider.value()))
        self.slider.setStyle(QStyleFactory.create('macintosh'))

        # play button
        self.pbtn = QPushButton('Play', self)
        self.pbtn.clicked.connect(self.playMusic)
        self.pbtn.setStyle(QStyleFactory.create('macintosh'))

        # preview button
        self.prebtn = QPushButton('Preview', self)
        self.prebtn.clicked.connect(self.previewMusic)
        self.prebtn.setStyle(QStyleFactory.create('macintosh'))

        # next button
        self.nbtn = QPushButton('Next', self)
        self.nbtn.clicked.connect(self.nextMusic)
        self.nbtn.setStyle(QStyleFactory.create('macintosh'))

        # open button
        self.obtn = QPushButton('Open file/folder..', self)
        self.obtn.clicked.connect(self.openDir)
        self.obtn.setStyle(QStyleFactory.create('macintosh'))

        # play list
        self.play_list = QListWidget()
        self.play_list.itemDoubleClicked.connect(self.doubleClicked)
        self.play_list.setStyle(QStyleFactory.create('macintosh'))
        self.loadconfig()

        # play mode
        self.play_mode = QComboBox()
        self.play_mode.addItem('Order')
        self.play_mode.addItem('Repeat once')
        self.play_mode.addItem('Shuffle')
        self.play_mode.setStyle(QStyleFactory.create('macintosh'))

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.selectPlayMode)
        self.timer.start(1000)

        # layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.play_list, 0, 0, 5, 10)
        self.grid.addWidget(self.label1, 0, 11, 1, 1)
        self.grid.addWidget(self.slider, 0, 12, 1, 1)
        self.grid.addWidget(self.label2, 0, 13, 1, 1)
        self.grid.addWidget(self.pbtn, 0, 14, 1, 1)
        self.grid.addWidget(self.nbtn, 1, 11, 1, 2)
        self.grid.addWidget(self.prebtn, 2, 11, 1, 2)
        self.grid.addWidget(self.play_mode, 3, 11, 1, 2)
        self.grid.addWidget(self.obtn, 4, 11, 1, 2)
        self.show()

    def errMessage(self, message):
        QMessageBox.about(self, 'Error:', message)

    def loadconfig(self):
        if os.path.isfile(self.config):
            config = configparser.ConfigParser()
            config.read(self.config)
            self.cur_path = config.get('song_list', 'PATH')
            self.showSongList()

    def updateconfig(self):
        config = configparser.ConfigParser()
        config.read(self.config)
        if not os.path.isfile(self.config):
            config.add_section('song_list')
        config.set('song_list', 'PATH', self.cur_path)
        config.write(open(self.config, 'w'))

    def showSongList(self):
        self.play_list.clear()
        self.updateconfig()
        for song in os.listdir(self.cur_path):
            if song.split('.')[-1] in self.song_formats:
                self.song_list.append(
                    [song, os.path.join(self.cur_path, song).
                     replace('\\', '/')])
                self.play_list.addItem(song)
        self.play_list.setCurrentRow(0)

    def openDir(self):
        self.cur_path = QFileDialog.getExistingDirectory(
            self, 'Select file/folder..', self.cur_path)
        if self.cur_path:
            self.showSongList()

    def doubleClicked(self):
        self.switch = True
        self.slider.setValue(0)
        self.setCurPlaying()
        self.playMusic()
        self.switch = False

    def setCurPlaying(self):
        self.cur_playing_song = self.song_list[self.play_list.currentRow()][-1]
        # absolute path use QUrl.fromLocalFile here
        self.player.setMedia(QMediaContent(
            QUrl.fromLocalFile(self.cur_playing_song)))

    def playMusic(self):
        if self.play_list.count() == 0:
            self.errMessage('No playable music files in the current path')
            return
        if not self.player.isAudioAvailable():
            self.setCurPlaying()
        if self.pause or self.switch:
            self.player.play()
            self.pause = False
            self.pbtn.setText('Stop')
        elif not self.pause:
            self.player.pause()
            self.pause = True
            self.pbtn.setText('Play')

    def previewMusic(self):
        if self.play_list.count() == 0:
            self.errMessage('No playable music files in the current path')
            return
        self.slider.setValue(0)
        self.play_list.setCurrentRow(self.play_list.currentRow() - 1
                                     if self.play_list.currentRow() != 0
                                     else self.play_list.count() - 1)
        self.switch = True
        self.setCurPlaying()
        self.playMusic()
        self.switch = False

    def nextMusic(self):
        if self.play_list.count() == 0:
            self.errMessage('No playable music files in the current path')
            return
        self.slider.setValue(0)
        self.switch = True
        if self.play_list.currentRow() == self.play_list.count() - 1:
            self.play_list.setCurrentRow(0)
        else:
            self.play_list.setCurrentRow(self.play_list.currentRow() + 1)
        self.setCurPlaying()
        self.playMusic()
        self.switch = False

    def selectPlayMode(self):
        if self.play_list.count() == 0:
            return
        if not self.pause and not self.switch and \
                self.player.position() == self.player.duration():
            if self.play_mode.currentIndex() == 0:
                self.nextMusic()
            elif self.play_mode.currentIndex() == 1:
                self.slider.setValue(0)
                self.switch = True
                self.setCurPlaying()
                self.playMusic()
                self.switch = False
            elif self.play_mode.currentIndex() == 2:
                self.slider.setValue(0)
                self.switch = True
                self.play_list.setCurrentRow(
                    random.randint(0, self.play_list.count() - 1))
                self.setCurPlaying()
                self.playMusic()
                self.switch = False

        # display time and progress in real time
        if not self.pause and not self.switch:
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.player.duration())
            self.slider.setValue(self.slider.value() + 1000)
            if self.slider.value() > self.player.position() + 1000:
                self.player.setPosition(self.slider.value())
        self.label1.setText(time.strftime(
            '%M:%S', time.localtime(self.player.position() / 1000)))
        self.label2.setText(time.strftime(
            '%M:%S', time.localtime(self.player.duration() / 1000)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = musicplayer()
    sys.exit(app.exec_())
