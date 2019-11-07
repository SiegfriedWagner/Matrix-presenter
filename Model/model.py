import copy
import logging as log
import os
import pickle
import random
import json
import Resources
from Settings import Settings


class Model:

    def __init__(self):
        log.debug("Creating model at {}".format(self))
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
        self.current_video = None
        self.video_played = 0
        self.participant = None

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

    def createParticipant(self, name, gender):
        log.debug("Creating participant with name {}".format(name))
        self.participant = Participant(name, gender)


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
        log.debug('Got response {}'.format(matrice_picture_path))
        log.debug('Response video {}'.format(self.current_video))
        if self.participant is not None:
            self.participant.process_response(video, matrice_picture_path, response_time)

    def finish(self):
        if self.participant is not None:
            self.participant.save_result()


class Participant:
    __slots__ = ('name', 'gender', 'videos', 'matrices', 'correctness', 'response_times')

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.matrices = []
        self.videos = []
        self.correctness = []
        self.response_times = []

    def process_response(self, video, matrix, time):
        self.videos.append(video)
        self.matrices.append(matrix)
        if video == matrix:
            self.correctness.append('1')
        else:
            self.correctness.append('0')
        self.response_times.append(time)

    def save_result(self, path: str=None, data_header: bool=True) -> None:
        if path is None:
            path = str(Settings.log_save_directory) + '/' + self.name
        if os.path.exists(path):
            log.warning("Folder {} exist, data from current participant will be saved in {}".format(path,
                                                                                                    path +
                                                                                                    '.new'))
            path += '.new'
        try:
            os.makedirs(path)
            with open(path + '/data.csv', 'w') as f:
                if data_header:
                    f.write("# matrix_number, video_number, response_time, correctness\n")
                for matrix, video, resp, corr in zip(self.matrices,
                                                     self.videos,
                                                     self.response_times,
                                                     self.correctness):
                    f.writelines("{}, {}, {:.3f}, {}\n".format(matrix, video, resp,
                                                      corr))  # TODO: Check in windows if \r is required
            with open(path + '/meta.json', 'w') as f:
                retu = Settings.to_dict()
                retu['gender'] = self.gender
                retu['name'] = self.name
                f.write(json.dumps(retu, indent=2))
        except IOError:
            dump_file = './' + self.name + '.dump'
            with open(dump_file, 'wb') as f:
                pickle.dump(self, f)
            log.critical("IOError occured, participant was dumped into " + str(dump_file))