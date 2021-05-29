import requests
import json

file = {'photo': open('CHI_0192.JPG', 'rb')}
data = {'latitude': 1.0, 'longitude': 2.0}
context = requests.post('http://127.0.0.1:8000/upload', files=file, data=data)
# context = requests.get('http://127.0.0.1:8000/events')
print(context.text)