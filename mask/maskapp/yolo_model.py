import torch


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YoloModel(metaclass=Singleton):
    def __init__(self):
        self.__model = torch.hub.load(repo_or_dir='./yolov5',source='local' , model='custom', path='./maskapp/weights/best.pt')
        #self.__model.conf = 0.4

    @property
    def model(self):
        return self.__model