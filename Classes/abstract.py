import abc


class ABCController(abc.ABC):

    def __init__(self, parent, name, view, model):
        self.parent = parent
        self.name = name
        self.view = view
        self.model = model


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
