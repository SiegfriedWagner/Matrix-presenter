import configparser
import os
import json
from Classes.abstract import Singleton
from Classes.descriptors import GreaterThanZero, Validated
import logging as log
import Resources
order_of_videos_options = ['sorted', 'random', 'two batches, random']
order_of_matrices_options = ['sorted']
language_options = Resources.languages

class _Settings(metaclass=Singleton):
    __slots__ = (
        '__config_file', '_number_of_videos', '_order_of_videos', '_order_of_matrices', '_duration_of_matrices',
        '_progressbar_height', '_time_resolution', '_save_directory', '_lang', '_tutorial_duration_of_matrices',
        '_fixation_cross_duration', '_starting_batch')

    number_of_videos = GreaterThanZero('_number_of_videos')
    order_of_videos = Validated('_order_of_videos', order_of_videos_options)
    order_of_matrices = Validated('_order_of_matrices', order_of_matrices_options)
    duration_of_matrices = GreaterThanZero('_duration_of_matrices')
    progressbar_height = GreaterThanZero('_progressbar_height')
    time_resolution = GreaterThanZero('_time_resolution')
    language = Validated('_lang', language_options)
    tutorial_duration_of_matrices = GreaterThanZero('_tutorial_duration_of_matrices')
    fixation_cross_duration = GreaterThanZero('_fixation_cross_duration')

    def __init__(self, filename=os.path.abspath('./Settings/settings.ini'), section_name='CUSTOM'):
        log.debug("Settings creation")
        self.__config_file = self.from_file(filename)
        config = self.__config_file
        self.number_of_videos = int(config[section_name]['number_of_videos'])
        self.order_of_videos = str(config[section_name]['order_of_videos'])
        self.order_of_matrices = str(config[section_name]['order_of_matrices'])
        self.duration_of_matrices = float(config[section_name]['duration_of_matrices'])
        self.progressbar_height = int(config['PROGRESSBAR']['HEIGHT'])
        self.time_resolution = float(config[section_name]['time_resolution'])
        self._save_directory = str(config[section_name]['log_save_directory'])
        self.language = str(config[section_name]['language'])
        self.tutorial_duration_of_matrices = float(config[section_name]['tutorial_duration_of_matrices'])
        self.fixation_cross_duration = float(config[section_name]['fixation_cross_duration'])

    @staticmethod
    def from_file(path: str):
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def save_to_file(self, path: str = "./Settings/settings.ini") -> None:
        for item in self.__config_file.items(self.__config_file.default_section):
            self.__config_file['CUSTOM'][item[0]] = str(getattr(self, item[0]))
        with open(path, 'w') as file:
            self.__config_file.write(file)

    def to_json(self, *args, **kwargs) -> str:
        ret = dict()
        for item in self.__config_file.items(self.__config_file.default_section):
            ret[str(item[0])] = str(getattr(self, item[0]))
        ret.pop('log_save_directory')
        return json.dumps(ret, *args, **kwargs)

    def to_dict(self,):
        ret = dict()
        for item in self.__config_file.items(self.__config_file.default_section):
            ret[str(item[0])] = str(getattr(self, item[0]))
        ret.pop('log_save_directory')
        return ret
    @property
    def log_save_directory(self) -> str:
        return self._save_directory


Settings = _Settings()
