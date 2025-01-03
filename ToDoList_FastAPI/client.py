import requests

# response = requests.post(f" http://127.0.0.1:8000/api/v1/user",
#                          json={"name": "user_1", "password": "1234"})
#
# print(response.status_code)
# print(response.json())


# response = requests.post(f" http://127.0.0.1:8000/api/v1/login",
#                          json={"name": "user_1", "password": "1234"})
#
# print(response.status_code)
# print(response.json())


# response = requests.post(f" http://127.0.0.1:8000/api/v1/todo",
#                          json={"title": "my todo_1", "description": "simple description", "important": False},
#                          headers={"x-token": '95b49320-7f66-4b9b-a995-08a4d9b7cb02'}
#                          )
#
# print(response.json())


response = requests.get(f" http://127.0.0.1:8000/api/v1/todo/1")

print(response.json())