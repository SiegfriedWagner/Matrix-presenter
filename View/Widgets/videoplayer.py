import logging as log

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QSizePolicy, QWidget

from Classes.descriptors import FuncDescriptor



class VideoPlayer(QVideoWidget):
    onVideoStop = FuncDescriptor()
    onVideoStart = FuncDescriptor()
    onVideoPause = FuncDescriptor()

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.stateChanged.connect(self.onStateChanged)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self._video_path = None

    @property
    def video_path(self):
        return self._video_path

    @video_path.setter
    def video_path(self, value):
        log.debug(" _video_path set to {}".format(value))
        self._video_path = value
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self._video_path)))

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)
        log.debug('{}.showEvent()')
        self.mediaPlayer.play()

    def onStateChanged(self):
        """
        0 - StoppedState
        1 - PlayingState
        2 - PausedState
        """
        state = self.mediaPlayer.state()
        if state == 0:
            self.onVideoStop()
        elif state == 1:
            self.onVideoStart()
        elif state == 2:
            self.onVideoPause()
        else:
            raise ValueError("Unknown state {}".format(state))

    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        log.debug("Close {}".format(self))

