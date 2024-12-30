import requests

response = requests.post(" http://127.0.0.1:8080/api/v1/todo",
                         json={"title": "t_1", "description": "d_1", "important": False}
                         )

print(response.status_code)
todo_id = response.json()['id']

response = requests.patch(f" http://127.0.0.1:8080/api/v1/todo/{todo_id}",
                         json={"done": True}
                         )

response = requests.get(f" http://127.0.0.1:8080/api/v1/todo/{todo_id}",
                         json={"done": True}
                         )
print(response.json())