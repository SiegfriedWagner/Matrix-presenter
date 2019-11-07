from Settings import Settings
import abc
class Text(abc.ABC):

    @property
    @abc.abstractmethod
    def introduction(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def description(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def example(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def example(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def correct(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def incorrect(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def end_of_tutorial(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def close(self):
        raise NotImplementedError
exec('from .{} import *'.format(Settings.language))

class Language(Text):
    @property
    def introduction(self):
        return introduction

    @property
    def description(self):
        return description.format(duration_of_matrices=Settings.duration_of_matrices)

    @property
    def example(self):
        return example


    @property
    def correct(self):
        return correct

    @property
    def incorrect(self):
        return incorrect

    @property
    def end_of_tutorial(self):
        return end_of_tutorial
    @property
    def close(self):
        return close
text: Text = Language()