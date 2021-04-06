import time
import Settings
import Resources
from Controller import ExperimentController
from Model import Model
from View import ExperimentView
from View.Widgets import Matrix
from Classes.logging import exp_logger


class TutorialController(ExperimentController):

    def __init__(self, parent, name, model: Model, view: ExperimentView):
        super().__init__(parent, name, model, view)
        self.timeout = -1

    def init_functionality(self):
        self.view.video_widget.mediaPlayer.setVolume(0)
        self.view.video_widget.onVideoStop = self.videoStop
        self.view.matrices_widget.on_show = self.matriceGridShow
        self.tutorial_precedure = self.tutorial_generator()
        next(self.tutorial_precedure)

    def matrixPush(self, matrix: Matrix, *args, **kwargs):
        if self.timer.isActive():
            self.timer.stop()
        #self.view.text_panel.setContent(Resources.text.correct)
        self.view.text_panel.setContent(Resources.text.end_of_tutorial)
        next(self.tutorial_precedure)

    def tutorial_generator(self):
        self.view.text_panel.setContent(Resources.text.introduction)
        self.view.text_panel.on_click = lambda :next(self.tutorial_precedure)
        exp_logger.info("Tutorial: introduction")
        yield
        self.view.text_panel.setContent(Resources.text.description)
        exp_logger.info("Tutorial: description")
        yield
        self.timeout = Settings.Settings.tutorial_duration_of_matrices
        self.view.changePanelTo(self.view.matrices_widget)
        exp_logger.info("Tutorial: matrices")
        yield
        self.view.text_panel.setContent(Resources.text.example)
        self.view.changePanelTo(self.view.text_panel)
        exp_logger.info("Tutorial: Example task")
        yield
        self.timeout = Settings.Settings.duration_of_matrices
        for matrix in self.view.matrices_widget.matrices:
            matrix.on_click = self.matrixPush, {'matrix': matrix}
        self.view.video_widget.video_path = self.model._Model__tutorial_video
        self.view.changePanelTo(self.view.video_widget)
        exp_logger.info(f"Tutorial: playing video: {self.model._Model__tutorial_video}")
        yield
        self.view.changePanelTo(self.view.text_panel)
        # yield
        # self.view.text_panel.setContent(Resources.text.end_of_tutorial)
        yield
        self.on_finish()
        exp_logger.info("Tutorial: end ")
        yield

    def timerEvent(self, QTimerEvent):
        value = time.time() - self._start_time
        if value > self.timeout:
            if self.timer.isActive():
                self.timer.stop()
            self.missAnswer()
        elif self.view.matrices_widget.progress_bar.value() != value and value > 0:
            self.valueChangeSignal.emit(
                int(value * self.view.matrices_widget.progress_bar.maximum() / self.timeout))

    def missAnswer(self):
        self.timer.stop()
        #self.view.text_panel.setContent(Resources.text.incorrect)
        self.view.text_panel.setContent(Resources.text.end_of_tutorial)
        next(self.tutorial_precedure)

