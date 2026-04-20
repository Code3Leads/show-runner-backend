import requests

url = "https://codemessaging.net/"

headers = {
    "User-Agent": "Mozilla/5.0"

}

response = request.get(url, headers=headers)

print(response.status_code)
print(response.text[:1000]) # print first part of page
