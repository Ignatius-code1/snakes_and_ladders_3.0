# Snakes and Ladders Game Backend
# Simple Flask API for the classic board game

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from supabase import create_client
from dotenv import load_dotenv
import random
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to connect
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

# Connect to Supabase database
supabase = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_KEY')
)

# Setup JWT for user authentication
jwt = JWTManager(app)

# Game rules: where snakes and ladders are located
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 21, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

@app.route('/start-game', methods=['POST'])
@jwt_required()
def start_new_game():
    """Start a fresh game for the logged-in player"""
    player_id = get_jwt_identity()
    
    # Create a new game in the database
    new_game = supabase.table('games').insert({'winner_id': None}).execute()
    game_id = new_game.data[0]['id']
    
    # Get the player's username
    player_info = supabase.table('users').select('username').eq('id', player_id).execute()
    player_name = player_info.data[0]['username']
    
    # Add the player to this game at starting position (0)
    supabase.table('game_players').insert({
        'game_id': game_id,
        'user_id': player_id,
        'username': player_name,
        'position': 0
    }).execute()
    
    return jsonify({'game_id': game_id, 'message': f'New game started for {player_name}!'})

@app.route('/roll-dice', methods=['POST'])
@jwt_required()
def roll_the_dice():
    """Roll dice and move the player"""
    data = request.get_json()
    game_id = data.get('game_id')
    player_id = get_jwt_identity()
    
    # Roll a dice (1 to 6)
    dice_roll = random.randint(1, 6)
    
    # Find the player in this game
    player_data = supabase.table('game_players').select('*').eq('game_id', game_id).eq('user_id', player_id).execute()
    player = player_data.data[0]
    
    # Calculate new position
    current_spot = player['position']
    new_spot = current_spot + dice_roll
    
    # Game rule: can't go past square 100
    if new_spot > 100:
        new_spot = current_spot  # Stay where you are
    
    # Check for snakes and ladders
    message = f"Rolled {dice_roll}!"
    if new_spot in snakes:
        new_spot = snakes[new_spot]
        message += " you hit a snake!"
    elif new_spot in ladders:
        new_spot = ladders[new_spot]
        message += " you found a ladder!"
    
    # Save the new position
    supabase.table('game_players').update({'position': new_spot}).eq('id', player['id']).execute()
    
    # Check if player won
    is_winner = False
    if new_spot == 100:
        supabase.table('games').update({'winner_id': player_id}).eq('id', game_id).execute()
        is_winner = True
        message += " 🎉 YOU WON!"
    
    return jsonify({
        'dice': dice_roll,
        'new_position': new_spot,
        'winner': is_winner,
        'message': message
    })

@app.route('/game-state', methods=['GET'])
@jwt_required()
def check_game_status():
    """Get current game information - who's where and who won"""
    game_id = request.args.get('game_id')
    
    # Get all players in this game
    all_players = supabase.table('game_players').select('*').eq('game_id', game_id).execute()
    game_info = supabase.table('games').select('winner_id').eq('id', game_id).execute()

    # Format player information nicely
    players = []
    for player in all_players.data:
        players.append({
            'user_id': player['user_id'],
            'name': player['username'],
            'position': player['position']
        })
    
    return jsonify({
        'players': players,
        'winner_id': game_info.data[0]['winner_id'],
        'game_id': game_id
    })

# Start the game server
if __name__ == '__main__':
    print("🎲 Snakes and Ladders server starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)