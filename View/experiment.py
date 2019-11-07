import logging

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QStackedWidget, QDialog, QHBoxLayout, QWidget

import Resources
from Model import Model
from View.Widgets.textpanel import TextPanel, FixationCross
from .Widgets.matricesgrid import MatricesGrid
from .Widgets.videoplayer import VideoPlayer


class ExperimentView(QDialog):


    def __init__(self, size, model):
        super().__init__()
        self.setFixedSize(size)  # TODO: Variable screensize
        self.stack = QStackedWidget(parent=self)
        self.stack.size = self.size
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.matrices_widget = MatricesGrid(model, parent=self)
        self.video_widget = VideoPlayer(parent=self)
        self.text_panel = TextPanel(parent=self, text=Resources.text.introduction)
        self.fixation_cross = FixationCross(parent=self)
        self.stack.addWidget(self.text_panel)
        self.stack.addWidget(self.video_widget)
        self.stack.addWidget(self.matrices_widget)
        self.stack.addWidget(self.fixation_cross)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.stack)
        self.setLayout(hbox)
        self.showFullScreen()

    def changePanelTo(self, widget: QWidget):
        self.stack.setCurrentWidget(widget)
        logging.debug('stack set to {}'.format(self.stack.currentWidget()))

    def addWidget(self, widget: QWidget):
        logging.debug('adding widget {} to stack'.format(widget))
        self.stack.addWidget(widget)

    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        logging.debug("Close {}".format(self))
