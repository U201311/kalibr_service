import requests

url = "http://localhost:8000/kalib/kalib_task"

response = requests.post(url)

try:
    response_json = response.json()
except ValueError:
    print("Response is not in JSON format")
    print("Response text:", response.text)
else:
    print(response_json)