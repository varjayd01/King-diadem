import requests

url = "http://localhost:8000/mobile/node"

data = {
 "location":"Bangkok",
 "food":60,
 "risk":30
}

r = requests.post(url,json=data)

print(r.json())
