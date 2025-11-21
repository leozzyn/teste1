import requests

SERVER_IP = "192.168.56.3"
URL_GET = f"http://{SERVER_IP}:5000/students"
URL_POST = f"http://{SERVER_IP}:5000/students/update"

def load_database():
    resp = requests.get(URL_GET)
    resp.raise_for_status()
    return resp.json()

def save_database(data):
    resp = requests.post(URL_POST, json=data)
    resp.raise_for_status()
    return resp.json()