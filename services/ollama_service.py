import requests

def ask_granite(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "granite3.3:2b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=60)
    return response.json()["response"]
