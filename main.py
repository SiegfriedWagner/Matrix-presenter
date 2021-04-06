import sys
from PyQt5.QtWidgets import QApplication
from Controller import MainControler
from Model import Model
from View import MainView
import logging
from os.path import dirname, join
# logging.getLogger().setLevel(logging.DEBUG)
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        test = app.desktop().screenGeometry().size()
        view = MainView()
        model = Model()
        controller = MainControler(view=view, model=Model())
        sys.exit(app.exec_())
    except Exception as e:
        if model.participant is not None:
            backup_path = join(dirname(__file__), 'error')
            model.participant.save_result(backup_path)
            err_message = f"Application exit with critical error: {e}. " \
                          f"Experimental data saved in: {backup_path}"
            logging.critical(err_message)
            with open(join(backup_path, "error.log"), 'w') as f:
                f.write(err_message)