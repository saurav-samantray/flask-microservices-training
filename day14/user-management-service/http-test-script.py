import requests
import json
import time

url = "http://localhost:8080/api/auth"

payload = json.dumps({
  "email": "saurav@gmail.com",
  "password": "saurav"
})
headers = {
  'Content-Type': 'application/json'
}

iterations = 100
start = time.time()
for i in range(iterations):
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
print(f"Time taken for {iterations} number requests: {time.time() - start} seconds")