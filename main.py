import sys
from PyQt5.QtWidgets import QApplication
from Controller import MainControler
from View import MainView
import logging
# logging.getLogger().setLevel(logging.DEBUG)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = app.desktop().screenGeometry().size()
    view = MainView()
    controller = MainControler(view=view)
    sys.exit(app.exec_())