from PyQt5 import QtGui
from Settings import Settings
from PyQt5.QtGui import QFont, QShowEvent
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QSpacerItem
from PyQt5.uic import loadUi
import logging
from PyQt5.Qt import *
from PyQt5.QtCore import Qt, QTimer
from Classes import FuncDescriptor

class TextPanel(QFrame):
    on_click = FuncDescriptor()

    def __init__(self, parent,  text, font: str='Helvetica', font_size: int=32, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = QLabel(parent=self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setContent(text, font, font_size)
        layout = QHBoxLayout()
        layout.addSpacerItem(QSpacerItem(20,20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        layout.addWidget(self.label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setLayout(layout)
        self.setFixedSize(self.parent().size())
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def mousePressEvent(self, QMouseEvent):
        self.on_click()

    def setContent(self, text:str, font: str='Helvetica', font_size: int = 32) -> None:
        self.label.setText(text)
        self.label.setFont(QFont(font, font_size))

class FixationCross(TextPanel):

    def __init__(self, parent, font: str='Helvetica', font_size: int=48, *args, **kwargs):
        super().__init__(parent=parent, text="+", font=font, font_size=font_size, *args, **kwargs)
        self.timer = QTimer(parent=self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(5000) # TODO: Fix const value

    def showEvent(self, a0: QtGui.QShowEvent):
        self.timer.setInterval(Settings.fixation_cross_duration*1000)
        self.timer.start()
