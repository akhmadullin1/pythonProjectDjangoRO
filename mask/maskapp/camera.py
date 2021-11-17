import cv2

from maskapp.yolo_model import YoloModel

#
def gen(camera):
    model = YoloModel().model
    while True:
        ret, frame = camera.read()
        results = model(frame, size=320)
        results.render()
        ret, jpeg = cv2.imencode('.jpg', results.imgs[0])
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

