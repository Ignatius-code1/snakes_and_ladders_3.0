# Snakes and Ladders API Documentation

## Base URL: `http://localhost:5000`

## Authentication
All game endpoints require Bearer token in Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### POST /register
Register a new user
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### POST /login
Login user and get JWT token
```json
{
  "email": "user@example.com", 
  "password": "password123"
}
```
Returns: `access_token`, `user_id`, `email`

### POST /start-game
Start a new game (requires auth)
Returns: `game_id`

### POST /join-game/<game_id>
Join an existing game (requires auth)
Returns: `player_order`

### POST /roll-dice
Roll dice and move player (requires auth)
```json
{
  "game_id": 123
}
```
Returns: `dice_roll`, `new_position`, `message`, `winner`

### GET /game-state/<game_id>
Get current game state (requires auth)
Returns: Game info and all players' positions

## Game Rules
- Players start at position 0
- Roll 1-6 to move forward
- Snakes move you backward, ladders move you forward
- First to position 100 wins
- Landing exactly on 100 required to win