import requests

file = {'photo': open('251.jpg', 'rb')}
data = {'location': {'lat': 1.0, 'long': 2.0}}
context = requests.post('http://127.0.0.1:8000/upload', files=file, data=data)
print(context.text)