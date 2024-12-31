import requests

# response = requests.post(f" http://127.0.0.1:8000/api/v1/user",
#                          json={"name": "user_1", "password": "1234"})
#
# print(response.status_code)
# print(response.json())


response = requests.post(f" http://127.0.0.1:8000/api/v1/login",
                         json={"name": "user_1", "password": "1234"})

print(response.status_code)
print(response.json())