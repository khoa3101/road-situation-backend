from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from .apps import RoadConfig
from .models import Event

import pytz
import mimetypes
import json
import torch
import torchvision.transforms as tvtf
from torch.nn import Softmax
from PIL import Image
from io import BytesIO

vietnam = pytz.timezone('Etc/GMT-7')

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
    return int(label), pred_classes[0, label]

@api_view(['GET'])
def home(request):
    return HttpResponse('Authorized by Khoa N. A. Nguyen and E-Ro Nguyen')

def get_events(request):
    res = []
    events = Event.objects.all()
    for event in events:
        img_name = event.IMAGE.url.split('/')[-1]
        res.append({
            'id': event.ID,
            'label': event.LABEL,
            'location': {
                'latitude': event.LAT,
                'longitude': event.LONG
            },
            'time': event.TIME.astimezone(vietnam).strftime('%d/%m/%Y %H:%M:%S'),
            'url': f'http://{settings.ALLOWED_HOSTS[0]}/image?name={img_name}'
        })
    return HttpResponse(json.dumps(res))

def get_image(request):
    image_name = request.GET['name']
    image_path = settings.MEDIA_ROOT.joinpath(f'images/{image_name}')
    
    try:
        img = open(image_path, 'rb')
        mime_type, _ = mimetypes.guess_type(image_path)
        response = HttpResponse(img, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={image_name}'
        return response
    except:
        return HttpResponse('No such file')

def delete_item(request):
    idx = request.GET['id']
    try:
        item = Event.objects.get(pk=idx)
        item.delete()
        return HttpResponse(f'Deleted {idx} successfully')
    except:
        return HttpResponse('Not existed')
    

@api_view(['POST'])
def post_image(request):
    img_io = BytesIO()
    img_name = str(len(Event.objects.all()) + 1).zfill(5) + '.jpg'
    # Get the file from post request
    try:
        img = request.FILES['image']
        img = Image.open(img).convert('RGB')
        label, _ = classify(RoadConfig.model, img.copy())
        if not label == 0:
            lat = request.data['latitude']
            long = request.data['longitude']
            img.save(img_io, format='JPEG', quality=100)
            img_content = ContentFile(img_io.getvalue(), img_name)

            new_event = Event(LABEL=label, LAT=lat, LONG=long, IMAGE=img_content)
            new_event.save()
        
        return HttpResponse(label)
    except:
        return HttpResponse('Not suitable image')