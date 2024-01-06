import requests

def make_req(prompt):
    headers = {
        "user_input": prompt
    }
    result = requests.post("http://127.0.0.1:5000/api/generate_response", json=headers)
    if result.status_code == 200:
        return result.json()['response']

def reset():
    result = requests.post("http://127.0.0.1:5000/api/reset_context")
    if result.status_code == 200:
        return True
