from django.http.response import ResponseHeaders
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from .apps import RoadConfig
from .models import Event

import json
import os
import torch
import torchvision.transforms as tvtf
from torch.nn import Softmax
from PIL import Image

categories = ['Bình thường', 'Cây ngã', 'Hỏa hoạn', 'Ngập lụt', 'Đường xấu', 'Kẹt xe', 'Rác thải', 'Tai nạn giao thông']

def classify(model, img):
    transforms = tvtf.Compose([
        tvtf.Resize((224, 224)),
        tvtf.ToTensor(),
        tvtf.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]),
    ])
    img = transforms(img).unsqueeze(0).to(RoadConfig.device)
    out = model(img)
    pred_classes = Softmax()(out)
    label = torch.argmax(pred_classes)
    return label, pred_classes[0, label]

@api_view(['GET'])
def home(request):
    return HttpResponse('Authorized by Khoa N. A. Nguyen and E-Ro Nguyen')

def get_events(request):
    res = []
    events = Event.objects.all()
    for event in events:
        res.append({
            'id': event.ID,
            'name': event.NAME,
            'location': {
                'latitude': event.LAT,
                'longitude': event.LONG
            }
        })
    return HttpResponse(json.dumps(res))

@api_view(['POST'])
def get_image(request):
    # Get the file from post request
    img = request.FILES['photo']
    img = Image.open(img).convert('RGB')

    label, _ = classify(RoadConfig.model, img)
    if not label == 0:
        location = request.data['location']
        lat = location['latitude']
        long = location.data['longitude']

        new_event = Event(NAME=categories[label], LAT=lat, LONG=long)
        new_event.save()
    
    return HttpResponse(categories[label])