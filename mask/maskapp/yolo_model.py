import torch


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YoloModel(metaclass=Singleton):
    def __init__(self):
        self.__model = torch.hub.load('ultralytics/yolov5', 'custom', path='./maskapp/weights/best.pt').autoshape()

    @property
    def model(self):
        return self.__model