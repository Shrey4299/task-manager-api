import requests

url = 'http://localhost:8000/api/tasks/'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNzA5NjE5NDE0LCJpYXQiOjE3MDcwMjc0MTR9.kbmIY6eZi01DOcEbOdeFvqq-45M1K2MvjSPRg52_KiQ'
}

data = {
    "title": "Your Task Title 4",
    "description": "Your task description goes here 2.",
    "due_date": "2024-02-10T12:00:00",
    "status": "Pending"
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Task created successfully:")
    print(response.json())
else:
    print("Error creating task:")
    print(response.status_code, response.text)
