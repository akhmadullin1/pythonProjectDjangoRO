import cv2

from maskapp.yolo_model import YoloModel, Singleton


class WebCamera():
    model = YoloModel().model

    def __init__(self, camera=None):
        self.__camera = camera

    def get_camera(self):
        return self.__camera

    def gen(self):
        while self.__camera is not None:
            ret, frame = self.__camera.read()
            results = self.model(frame, size=320)
            results.render()
            ret, jpeg = cv2.imencode('.jpg', results.imgs[0])
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

