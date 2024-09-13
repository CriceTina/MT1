
import requests
import json

url = "http://192.168.148.124:11434/api/chat"


def llama3(prompt):
    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }],
        "stream": False
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        print(f"Error: {response.status_code}")
        return None


