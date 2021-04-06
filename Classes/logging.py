import logging as _logging
from Settings import Settings
import os.path as p
exp_logger = _logging.getLogger('exp_logger')
exp_logger.setLevel(_logging.INFO)


def set_file_handler(participant_name: str):
    # clear old handlers
    if exp_logger.hasHandlers():
        for handler in exp_logger.handlers:
            exp_logger.removeHandler(handler)
    # add new handler based on participant name and settings
    path = p.join(str(Settings.log_save_directory), participant_name, "experiment_log.log")
    exp_logger.addHandler(_logging.FileHandler(path, 'a', 'UTF-8', False))
