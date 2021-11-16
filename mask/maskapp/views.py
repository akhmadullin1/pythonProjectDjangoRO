import os

from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
import argparse
import io
import torch
from maskapp.yolo_model import YoloModel
# Create your views here.


def index(request):
    return render(request, 'maskapp/about.html', {'name': 2})


def mask_img(request):

    if request.method == "POST" and request.FILES['file']:

        model = YoloModel().model  # Обученная модель

        file = request.FILES["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)
        results.render()

        pics = [os.path.join('./maskapp/static/maskapp/uploadpic/', x) for x in os.listdir('./maskapp/static/maskapp/uploadpic/') if x[-3:] == "jpg"]
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