import copy
from Classes.logging import exp_logger
import logging
import os
import random
import json
import Resources
from Settings import Settings
import uuid


class Model:

    def __init__(self):
        logging.debug("Creating model at {}".format(self))
        self.current_video = None
        self.video_played = 0
        self.participant = None
        self.__matrices = []

    @property
    def matrices(self):
        if len(self.__matrices) != 20: #TODO: Hardcoded value
            raise ValueError("Not enough matrices, please make sure that there are 20 matrix pictures in ./Resources/images directory")
        return copy.deepcopy(self.__matrices)

    @property
    def videos(self):
        if len(self.__videos) < Settings.number_of_videos:
            raise ValueError(f"Not enough films, please make sure that there are enough ({Settings.number_of_videos} required) video files in Resources/videos directory")
        return copy.deepcopy(self.__videos)

    def create_participant(self, name, gender):
        exp_logger.info(f"Creating participant with name {name}")
        self.participant = Participant(name, gender)
        self.video_played = 0
        self.participant.enable_saving()

    def video_generator(self, num_of_videos=None):
        if num_of_videos is None:
            num_of_videos = Settings.number_of_videos
        if num_of_videos > len(self.videos):
            raise ValueError("There is only " + str(len(self.videos)) + " films, but required is " + str(num_of_videos))
        i = 0
        videos = iter(self.videos)
        while i != num_of_videos:
            self.current_video = next(videos)
            yield self.current_video
            i += 1

    def get_response(self, matrice_picture_path: str = None, response_time=None):
        if matrice_picture_path is None:
            matrice_picture_path = 'None'
        else:
            matrice_picture_path = os.path.basename(matrice_picture_path)
            matrice_picture_path, _ = matrice_picture_path.split('.')
        if response_time is None:
            response_time = 0
        video = os.path.basename(self.current_video)
        video, _ = video.split('.')
        logging.debug('Got response {}'.format(matrice_picture_path))
        logging.debug('Response video {}'.format(self.current_video))
        if self.participant is not None:
            self.participant.process_response(video, matrice_picture_path, response_time)

    def load_settings(self):
        if Settings.order_of_matrices == 'sorted':
            self.__matrices = sorted(Resources.images)
        else:
            raise NotImplementedError("Option {} is not implemented.".format(Settings.duration_of_matrices))
        if Settings.order_of_videos == 'sorted':
            self.__videos = sorted(Resources.get_videos())
            self.__tutorial_video = self.__videos.pop(0)
        elif Settings.order_of_videos == 'random':
            self.__videos = sorted(Resources.get_videos())
            self.__tutorial_video = self.__videos.pop(0)
            random.shuffle(self.__videos)
        elif Settings.order_of_videos == 'two batches, random':
            self.__videos = Resources.get_videos()
            self.__tutorial_video = self.__videos.pop(0)
        else:
            raise NotImplementedError("Option {} is not implemented.".format(Settings.order_of_videos))


class Participant:
    __slots__ = ('name', 'gender', 'experiment_data_logger')

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.experiment_data_logger = logging.getLogger(f'data_logger_{uuid.uuid4()}')
        self.experiment_data_logger.setLevel(logging.INFO)

    def enable_saving(self, path: str = None, data_header: bool = True) -> None:
        if path is None:
            path = str(Settings.log_save_directory) + '/' + self.name
        if os.path.exists(path):
            logging.warning("Folder {} exist, data from current participant will be saved in {}".format(path,
                                                                                                    path +
                                                                                                    '.new'))
            path += '.new'
            self.enable_saving(path, data_header)
            return 
        os.makedirs(path)
        csv_path = os.path.join(path, 'data.csv')
        file_handler = logging.FileHandler(csv_path, 'a', 'UTF-8', False)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        self.experiment_data_logger.addHandler(file_handler)
        if data_header:
            self.experiment_data_logger.info("# matrix_number, video_number, response_time, correctness")
        with open(os.path.join(path, "meta.json",), 'w') as f:
            retu = Settings.to_dict()
            retu['gender'] = self.gender
            retu['name'] = self.name
            f.write(json.dumps(retu, indent=2))
        exp_logger.info(f"Saving records enabled. Csv file path {csv_path}")

    def process_response(self, video, matrix, response_time):
        if video == matrix:
            correct = '1'
        else:
            correct = '0'
        self.experiment_data_logger.info("{}, {}, {:.3f}, {}".format(
            matrix, video, response_time, correct))
