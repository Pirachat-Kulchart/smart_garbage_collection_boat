import requests

def send_to_external_api(data):
    url = 'http://external-api-url/endpoint'
    response = requests.post(url, json=data)
    return response.json()  # หรือใช้ response.text หากไม่ต้องการแปลงเป็น JSON
