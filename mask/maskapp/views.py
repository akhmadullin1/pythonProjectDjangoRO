import os
import cv2

from django.http import HttpResponse, StreamingHttpResponse

from django.shortcuts import render
from PIL import Image
import argparse
import io
import torch
from maskapp.yolo_model import YoloModel
from maskapp.camera import WebCamera

# Create your views here.
cam = WebCamera(cv2.VideoCapture(0))


def index(request):
    global cam
    if cam.get_camera():
        cam.get_camera().release()
    return render(request, 'maskapp/about.html', {'name': 2})


def mask_img(request):
    global cam
    if cam.get_camera():
        cam.get_camera().release()
    if request.method == "POST" and request.FILES['file']:

        model = YoloModel().model  # Обученная модель

        file = request.FILES["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=320)
        results.render()

        pics = [os.path.join('./maskapp/static/maskapp/uploadpic/', x) for x in
                os.listdir('./maskapp/static/maskapp/uploadpic/') if x[-3:] == "jpg"]
        pics.sort(key=lambda x: int(x.split('image')[1].split('.')[0]))
        path = os.path.abspath("./maskapp/static/maskapp/uploadpic/image" + str(len(pics)) + ".jpg")
        static_path = "/static/maskapp/uploadpic/image" + str(len(pics)) + ".jpg"

        for img in results.imgs:
            img_base64 = Image.fromarray(img)

            img_base64.save(path, format="JPEG")
        return render(request, 'maskapp/image.html', {'path': static_path})

    return render(request, 'maskapp/image.html')


def mask_vid(request):
    return render(request, 'maskapp/video.html', {'name': 2})


def video_feed(request):
    global cam
    cam = WebCamera(cv2.VideoCapture(0))
    webcam = cam.get_camera()

    if not (webcam is None or not webcam.isOpened()):
        return StreamingHttpResponse(cam.gen(), content_type='multipart/x-mixed-replace; boundary=frame')
    else:

        return HttpResponse()
