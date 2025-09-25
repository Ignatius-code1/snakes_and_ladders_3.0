from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase_config import supabase
from functools import wraps
import random

app = Flask(__name__)
CORS(app)

SNAKES_LADDERS = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78,
    1: 38, 4: 14, 9: 21, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100
}

@app.route('/')
def home():
    return jsonify({
        'message': 'Snakes and Ladders API',
        'endpoints': {
            'POST /register': 'Register new user',
            'POST /login': 'Login user',
            'POST /start-game': 'Start new game',
            'POST /roll-dice': 'Roll dice',
            'GET /game-state/<game_id>': 'Get game state'
        }
    })

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            user = supabase.auth.get_user(token.split(' ')[1])
            request.current_user = user.user
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return jsonify({'message': 'User created successfully', 'user': response.user.email}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return jsonify({
            'access_token': response.session.access_token,
            'user_id': response.user.id,
            'email': response.user.email
        })
    except Exception as e:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/start-game', methods=['POST'])
@auth_required
def start_game():
    user_id = request.current_user.id
    
    # Create new game
    game_result = supabase.table('games').insert({
        'current_turn': 0,
        'is_active': True
    }).execute()
    
    game_id = game_result.data[0]['id']
    
    # Add player to game
    supabase.table('game_players').insert({
        'game_id': game_id,
        'user_id': user_id,
        'position': 0,
        'player_order': 0
    }).execute()
    
    return jsonify({'game_id': game_id, 'message': 'Game started successfully'})

@app.route('/join-game/<int:game_id>', methods=['POST'])
@auth_required
def join_game(game_id):
    user_id = request.current_user.id
    
    # Check if game exists and is active
    game = supabase.table('games').select('*').eq('id', game_id).eq('is_active', True).execute()
    if not game.data:
        return jsonify({'error': 'Game not found or not active'}), 404
    
    # Check if user already in game
    existing = supabase.table('game_players').select('*').eq('game_id', game_id).eq('user_id', user_id).execute()
    if existing.data:
        return jsonify({'error': 'Already in this game'}), 400
    
    # Get next player order
    players = supabase.table('game_players').select('*').eq('game_id', game_id).execute()
    next_order = len(players.data)
    
    # Add player to game
    supabase.table('game_players').insert({
        'game_id': game_id,
        'user_id': user_id,
        'position': 0,
        'player_order': next_order
    }).execute()
    
    return jsonify({'message': 'Joined game successfully', 'player_order': next_order})

@app.route('/roll-dice', methods=['POST'])
@auth_required
def roll_dice():
    user_id = request.current_user.id
    data = request.get_json()
    game_id = data.get('game_id')
    
    # Get current game and player
    game = supabase.table('games').select('*').eq('id', game_id).execute()
    player = supabase.table('game_players').select('*').eq('game_id', game_id).eq('user_id', user_id).execute()
    
    if not game.data or not player.data or not game.data[0]['is_active']:
        return jsonify({'error': 'Invalid game or game finished'}), 400
    
    # Roll dice
    dice_roll = random.randint(1, 6)
    current_position = player.data[0]['position']
    new_position = current_position + dice_roll
    
    # Check if player wins
    winner = False
    if new_position >= 100:
        new_position = 100
        winner = True
        supabase.table('games').update({'winner_id': user_id, 'is_active': False}).eq('id', game_id).execute()
    
    # Apply snakes and ladders
    final_position = SNAKES_LADDERS.get(new_position, new_position)
    
    # Update player position
    supabase.table('game_players').update({'position': final_position}).eq('game_id', game_id).eq('user_id', user_id).execute()
    
    result = {'dice_roll': dice_roll, 'new_position': final_position, 'message': ''}
    
    if new_position in SNAKES_LADDERS:
        result['message'] = 'Snake! 🐍' if SNAKES_LADDERS[new_position] < new_position else 'Ladder! 🪜'
    
    if winner:
        result['message'] = 'Winner! 🎉'
        result['winner'] = True
    
    return jsonify(result)

@app.route('/game-state/<int:game_id>', methods=['GET'])
@auth_required
def game_state(game_id):
    user_id = request.current_user.id
    
    # Check if user is in this game
    player_check = supabase.table('game_players').select('*').eq('game_id', game_id).eq('user_id', user_id).execute()
    if not player_check.data:
        return jsonify({'error': 'Not authorized for this game'}), 403
    
    # Get game info
    game = supabase.table('games').select('*').eq('id', game_id).execute()
    players = supabase.table('game_players').select('*, users(email)').eq('game_id', game_id).execute()
    
    return jsonify({
        'game_id': game_id,
        'current_turn': game.data[0]['current_turn'],
        'winner_id': game.data[0].get('winner_id'),
        'is_active': game.data[0]['is_active'],
        'players': [{
            'user_id': p['user_id'],
            'email': p['users']['email'],
            'position': p['position'],
            'player_order': p['player_order']
        } for p in players.data]
    })

if __name__ == '__main__':
    app.run(debug=True)