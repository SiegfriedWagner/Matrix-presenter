import logging as log
import time
import Classes.abstract
import Resources
import Settings
from PyQt5.QtCore import QTimer, QBasicTimer, pyqtSignal, QObject
from PyQt5.QtGui import QMouseEvent

from Classes import FuncDescriptor
from View.experiment import ExperimentView
from View.Widgets.matricesgrid import Matrix
from View.Widgets.videoplayer import VideoPlayer
from Model.model import Model



class ExperimentController(QObject):
    valueChangeSignal = pyqtSignal(int)
    on_finish = FuncDescriptor()
    def __init__(self, parent, name, model: Model, view: ExperimentView):
        super().__init__(parent=parent)
        log.debug('Init ExperimentController')
        self.view = view
        self.name = name
        self.model = model
        self.timer = QBasicTimer()
        self.valueChangeSignal.connect(self.view.matrices_widget.progress_bar.setValue)
        self._start_time = -1
        self.init_functionality()

    def init_functionality(self):
        self.video_generator = self.model.video_generator()
        self.view.video_widget.video_path = next(self.video_generator)
        self.view.video_widget.mediaPlayer.setVolume(0)
        for matrix in self.view.matrices_widget.matrices:
            matrix.on_click = self.matrixPush, {'matrix': matrix}
        self.view.video_widget.onVideoStop = self.videoStop
        self.view.matrices_widget.on_show = self.matriceGridShow
        self.view.text_panel.setContent(Resources.text.close)
        self.view.text_panel.on_click = self.view.close
        self.view.changePanelTo(self.view.fixation_cross)
        self.view.fixation_cross.timer.timeout.connect(lambda :self.view.changePanelTo(self.view.video_widget))

    def matrixPush(self, matrix: Matrix, *args, **kwargs):
        log.debug('Called matricePush')
        self.model.get_response(matrice_picture_path=matrix.name, response_time=time.time() - self._start_time)
        if self.timer.isActive():
            self.timer.stop()
        try:
            self.view.video_widget.video_path = next(self.video_generator)
            self.view.changePanelTo(self.view.fixation_cross)
        except StopIteration: #TODO remove duplicate
            self.model.finish()
            self.view.changePanelTo(self.view.text_panel)


    def videoStop(self):
        self.view.changePanelTo(self.view.matrices_widget)

    def matriceGridShow(self):
        log.debug('called matriceGridShow')
        self._start_time = time.time()
        self.timer.start(Settings.Settings.time_resolution, self)

    def timerEvent(self, QTimerEvent):
        value = time.time() - self._start_time
        log.debug("called processTimer, time: {}".format(value))
        if value > Settings.Settings.duration_of_matrices:
            self.missAnswer()
        elif self.view.matrices_widget.progress_bar.value() != value and value > 0:
            log.debug("Setting changebar value to:" + str(int(value * 1000 / Settings.Settings.duration_of_matrices)))
            self.valueChangeSignal.emit(int(value * 1000 / Settings.Settings.duration_of_matrices))
            self.view.update()

    def missAnswer(self):
        self.timer.stop()
        self.model.get_response()
        try:
            self.view.video_widget.video_path = next(self.video_generator)
            self.view.changePanelTo(self.view.fixation_cross)
        except StopIteration:
            self.model.finish()
            self.view.changePanelTo(self.view.text_panel)

