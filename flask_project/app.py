from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from supabase import create_client
from dotenv import load_dotenv
import random
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

supabase = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_KEY')
)

jwt = JWTManager(app)

# Where snakes and ladders are
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 21, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

@app.route('/start-game', methods=['POST'])
@jwt_required()
def start_game():
    player_id = get_jwt_identity()
    
    # Make new game
    game = supabase.table('games').insert({'winner_id': None}).execute()
    game_id = game.data[0]['id']
    
    # Get player name
    user = supabase.table('users').select('username').eq('id', player_id).execute()
    name = user.data[0]['username']
    
    # Add player to game
    supabase.table('game_players').insert({
        'game_id': game_id,
        'user_id': player_id,
        'username': name,
        'position': 0
    }).execute()
    
    return jsonify({'game_id': game_id})

@app.route('/roll-dice', methods=['POST'])
@jwt_required()
def roll_dice():
    data = request.get_json()
    game_id = data.get('game_id')
    player_id = get_jwt_identity()
    
    # Roll dice
    dice = random.randint(1, 6)
    
    # Get player
    player = supabase.table('game_players').select('*').eq('game_id', game_id).eq('user_id', player_id).execute()
    current_pos = player.data[0]['position']
    new_pos = current_pos + dice
    
    # Can't go past 100
    if new_pos > 100:
        new_pos = current_pos
    
    # Check snakes and ladders
    if new_pos in snakes:
        new_pos = snakes[new_pos]
    elif new_pos in ladders:
        new_pos = ladders[new_pos]
    
    # Update position
    supabase.table('game_players').update({'position': new_pos}).eq('id', player.data[0]['id']).execute()
    
    # Check winner
    winner = False
    if new_pos == 100:
        supabase.table('games').update({'winner_id': player_id}).eq('id', game_id).execute()
        
        # Add win
        user_stats = supabase.table('users').select('wins').eq('id', player_id).execute()
        wins = user_stats.data[0]['wins'] or 0
        supabase.table('users').update({'wins': wins + 1}).eq('id', player_id).execute()
        
        winner = True
    
    return jsonify({
        'dice': dice,
        'new_position': new_pos,
        'winner': winner
    })

@app.route('/game-state', methods=['GET'])
@jwt_required()
def game_state():
    game_id = request.args.get('game_id')
    
    # Get players
    players = supabase.table('game_players').select('*').eq('game_id', game_id).execute()
    game = supabase.table('games').select('winner_id').eq('id', game_id).execute()
    
    player_list = []
    for p in players.data:
        stats = supabase.table('users').select('wins, losses').eq('id', p['user_id']).execute()
        s = stats.data[0] if stats.data else {'wins': 0, 'losses': 0}
        
        player_list.append({
            'user_id': p['user_id'],
            'name': p['username'],
            'position': p['position'],
            'wins': s['wins'] or 0,
            'losses': s['losses'] or 0
        })
    
    return jsonify({
        'players': player_list,
        'winner': game.data[0]['winner_id']
    })

@app.route('/stats', methods=['GET'])
@jwt_required()
def stats():
    player_id = get_jwt_identity()
    
    user = supabase.table('users').select('username, wins, losses').eq('id', player_id).execute()
    p = user.data[0]
    
    return jsonify({
        'name': p['username'],
        'wins': p['wins'] or 0,
        'losses': p['losses'] or 0
    })

if __name__ == '__main__':
    app.run(debug=True)