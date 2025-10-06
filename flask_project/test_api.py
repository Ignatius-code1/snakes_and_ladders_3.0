import requests
import json

BASE_URL = "http://localhost:5000"

def test_register():
    response = requests.post(f"{BASE_URL}/register", json={
        "email": "michelle@test.com",
        "password": "password123"
    })
    print("Register:", response.status_code, response.json())

def test_login():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "michelle@test.com", 
        "password": "password123"
    })
    print("Login:", response.status_code, response.json())
    return response.json().get('access_token')

def test_game_flow(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # Start game
    response = requests.post(f"{BASE_URL}/start-game", headers=headers)
    print("Start Game:", response.status_code, response.json())
    game_id = response.json().get('game_id')
    
    # Roll dice
    response = requests.post(f"{BASE_URL}/roll-dice", 
                           json={"game_id": game_id}, headers=headers)
    print("Roll Dice:", response.status_code, response.json())
    
    # Get game state
    response = requests.get(f"{BASE_URL}/game-state/{game_id}", headers=headers)
    print("Game State:", response.status_code, response.json())

if __name__ == "__main__":
    test_register()
    token = test_login()
    if token:
        test_game_flow(token)