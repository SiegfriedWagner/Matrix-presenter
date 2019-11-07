import logging as log
from typing import List
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QProgressBar, QSizePolicy, QHBoxLayout, QLayout, QSpacerItem

import Settings
from Classes.descriptors import FuncDescriptor


class Matrix(QLabel):
    on_click = FuncDescriptor()

    def __init__(self, parent, picture, name=None):
        super().__init__(parent=parent)
        if name is None:
            name = picture
        self.pic: QPixmap = None
        self.name = str(name)
        pic = QPixmap()
        pic.load(picture)
        if pic.width() > pic.height():
            pic = pic.scaledToHeight(int(parent.height() / 4))  # TODO removed hardcoded value
        else:
            pic = pic.scaledToWidth(int(parent.width() / 5))  # TODO remove hardcoded value
        self.setPixmap(pic)

    def setPixmap(self, a0: QtGui.QPixmap):
        super().setPixmap(a0)
        super().setFixedSize(a0.size())
        self.pic = a0

    def setFixedSize(self, a0: QtCore.QSize):
        if self.pic is not None:
            self.pic.scaledToHeight(a0.height())
            super().setFixedSize(self.pic.size())
        else:
            super().setFixedSize(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.on_click()

class MatricesGrid(QWidget):
    on_show = FuncDescriptor()

    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.setFixedSize(self.parent().size())
        self.model = model
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        self._matrices = []
        self.matrice_grid = QWidget(parent=self)
        reduced = self.height() - Settings.Settings.progressbar_height

        self.matrice_grid.setFixedSize(self.width(), reduced)
        self.matrice_grid.setLayout(QVBoxLayout())
        self.matrice_grid.layout().setSpacing(0)
        self.matrice_grid.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(Settings.Settings.progressbar_height)
        self.progress_bar.setMaximum(1000)
        self.progress_bar.setMinimum(0)
        # self.progress_bar.setValue = self.setValue
        vbox.addWidget(self.matrice_grid)
        vbox.addWidget(self.progress_bar)
        matrices = self.model.matrices
        mat_iter = iter(matrices)
        for i in range(0, 4):  # TODO: Fix hardcoded numbers
            row = QHBoxLayout()
            row.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
            for j in range(0, 5):  # TODO Fix hardcoded values
                self.addMatrix(row, next(mat_iter))
            row.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
            self.matrice_grid.layout().addItem(row)

    def addMatrix(self, target, path):
        matrice = Matrix(parent=self.matrice_grid, picture=path)
        if isinstance(target, QWidget):
            target.layout().addWidget(matrice)
        elif isinstance(target, QLayout):
            target.addWidget(matrice)
        self._matrices.append(matrice)

    @staticmethod
    def setValue(obj, value):
        log.debug("Set value in progressbar: {}".format(value))
        super(obj).setValue(obj, value)

    @property
    def matrices(self) -> List[Matrix]:
        return self._matrices

    def get_matrices_size(self):
        width = self.matrice_grid.layout().columnCount() * self.matrices[0].width()
        height = self.matrice_grid.layout().rowCount() * self.matrices[0].height()
        return width, height

    def showEvent(self, a0: QtGui.QShowEvent):
        log.debug('called showEvent')
        super().showEvent(a0)
        self.on_show()

    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        log.debug("Close {}".format(self))
