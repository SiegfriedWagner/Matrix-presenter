from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import Settings
import Resources
import os
class MainView(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'main.ui'), self)
        self.orderOfVideosComboBox.addItems(Settings.order_of_videos_options)
        self.orderOfVideosComboBox.currentTextChanged.connect(self.on_batch_set)
        self.orderOfVideosComboBox.setCurrentText(Settings.Settings.order_of_videos)
        self.orderOfMatricesComboBox.addItems(Settings.order_of_matrices_options)
        self.orderOfMatricesComboBox.setCurrentText(Settings.Settings.order_of_matrices)
        self.numberOfVideosSpinBox.setValue(Settings.Settings.number_of_videos)
        self.matrixTimeSpinBox.setValue(Settings.Settings.duration_of_matrices)
        self.saveDirectoryLabel.setText(Settings.Settings.log_save_directory)
        self.participantGenderComboBox.addItems(['Man', 'Woman'])
        self.languageComboBox.addItems(Resources.languages)
        self.fixationCrossSpinBox.setValue(Settings.Settings.fixation_cross_duration)
        self.tutorialMatrixTimeSpinBox.setValue(Settings.Settings.tutorial_duration_of_matrices)
        self.show()

    def on_batch_set(self, text):
        if text == 'two batches, random':
            self.startingGroupLabel.show()
            self.startingGroupComboBox.clear()
            self.startingGroupComboBox.addItems(Resources.get_batches())
            self.startingGroupComboBox.show()
        else:
            self.startingGroupLabel.hide()
            self.startingGroupComboBox.hide()
