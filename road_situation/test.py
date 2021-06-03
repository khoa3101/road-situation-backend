import requests
import json
import datetime
import pytz


file = {'image': open('CHI_0192.JPG', 'rb')}
data = {'latitude': 1.5, 'longitude': 2.1}
# context = requests.post('http://517cea5bac81.ngrok.io/upload', files=file, data=data)
context = requests.get('http://517cea5bac81.ngrok.io/events')
# # context = requests.get('http://517cea5bac81.ngrok.io/delete?id=1')
print(context.text)