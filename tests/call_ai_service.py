import requests
import json

# Define the URL and the payload
url = "http://127.0.0.1:8001/aiMakeMove"

board_text = '''2 2
    1   2   3   4
    3   4   .   2
    2   1   .   3
    .   .   .   1
'''

payload = {
    "game_board": board_text.strip(),
    "ai_player": "minimax_player",
    "time_limit": 1
}

# Make the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    move = response.json()
    print("Move received:", move)
else:
    print("Error:", response.status_code)
