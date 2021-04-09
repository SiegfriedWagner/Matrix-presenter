import logging as log

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication

from Settings import Settings
from Controller.experiment import ExperimentController
from Controller.tutorial import TutorialController
from Model.model import Model
from View.experiment import ExperimentView
from View.main import MainView
from Resources import import_text
from Classes.logging import exp_logger, set_file_handler


class EmptyFieldException(ValueError):
    pass


class MainControler(QObject):

    def __init__(self, view: MainView, model: Model):
        super().__init__()
        self.model = model
        self.controllers = {'main': self}
        view.saveSettingsPushButton.clicked.connect(self.saveSettings)
        view.runExperimentPushButton.clicked.connect(self.runExperiment)
        view.saveDirectoryPushButton.clicked.connect(self.setSaveDirectory)
        self.views = {'main': view}

    def runExperiment(self, *args):
        try:
            self.getSettings()
            self.model.load_settings()
            import_text()
        except Exception as e:
            QMessageBox.warning(self.views['main'], "", e.args[0])
            log.debug(*e.args)
            return
        participant_code = self.views['main'].participantCodeLineEdit.text()
        self.model.create_participant(participant_code,
                                      self.views['main'].participantGenderComboBox.currentText())
        set_file_handler(participant_code)
        exp_logger.info("Experiment started")
        self.views['experiment'] = ExperimentView(model=self.model, size=QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen()).size())
        self._tutorial()

    def _tutorial(self):
        tut = TutorialController(parent=self, name='tutorial', model=self.model, view=self.views['experiment'])
        tut.on_finish = self._experiment
        self.controllers['tutorial'] = tut
        tut.view.exec_()

    def _experiment(self):
        if 'tutorial' in self.controllers.keys():
            self.controllers.pop('tutorial')
        exp = ExperimentController(parent=self, name='experiment', model=self.model, view=self.views['experiment'])
        #TODO casdaced funcdescriptor
        self.controllers['experiment'] = exp
        exp.view.exec_()

    def saveSettings(self):
        try:
            self.getSettings()
        except EmptyFieldException:
            pass
        Settings.save_to_file('./Settings/settings.ini')

    def getSettings(self):
        Settings.number_of_videos = self.views['main'].numberOfVideosSpinBox.value()
        Settings.order_of_videos = self.views['main'].orderOfVideosComboBox.currentText()
        Settings.order_of_matrices = self.views['main'].orderOfMatricesComboBox.currentText()
        Settings.duration_of_matrices = self.views['main'].matrixTimeSpinBox.value()
        Settings.fixation_cross_duration = self.views['main'].fixationCrossSpinBox.value()
        Settings.tutorial_duration_of_matrices = self.views['main'].tutorialMatrixTimeSpinBox.value()
        Settings.language = self.views['main'].languageComboBox.currentText()
        Settings._starting_batch = self.views['main'].startingGroupComboBox.currentText()
        participant_code = self.views['main'].participantCodeLineEdit.text()
        if participant_code == "":
            log.warning('Exception: Participant code null')
            raise EmptyFieldException('Participant code cannot be empty')

    def setSaveDirectory(self):
        diag = QFileDialog()
        diag.setFileMode(QFileDialog.Directory)
        filename = diag.getExistingDirectory(self.views['main'], "Folder do zapisu wyników", Settings.log_save_directory)
        self.views['main'].saveDirectoryLabel.setText(filename)
        Settings._save_directory = str(filename)
