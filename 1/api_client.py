import requests

def send_request(method: str, endpoint: str, payload: dict = None):
    url = f"http://localhost:8000{endpoint}"
    return requests.request(method=method, url=url, json=payload)
