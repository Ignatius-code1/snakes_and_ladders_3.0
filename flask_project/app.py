from flask import Flask, request, jsonify
from flask_cors import CORS
<<<<<<< HEAD
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
=======
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, Game, GamePlayer
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

# Snakes and Ladders positions
SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
LADDERS = {1: 38, 4: 14, 9: 21, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'message': 'Snakes and Ladders API is running', 'endpoints': ['/register', '/login', '/start-game', '/roll-dice', '/game-state/<game_id>', '/my-game']})

@app.route('/my-game', methods=['GET'])
@jwt_required()
def get_my_game():
    user_id = get_jwt_identity()
    
    # Find user's active game
    active_game = db.session.query(Game).join(GamePlayer).filter(
        GamePlayer.user_id == user_id,
        Game.is_active == True
    ).first()
    
    if active_game:
        return jsonify({'game_id': active_game.id, 'has_active_game': True})
    else:
        return jsonify({'has_active_game': False})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token, 'username': username}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401
>>>>>>> 440508f301fc3d3ac477f2c85e3a6cdd4790c167

@app.route('/start-game', methods=['POST'])
@jwt_required()
def start_game():
<<<<<<< HEAD
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
=======
    user_id = get_jwt_identity()
    
    # Create new game
    game = Game()
    db.session.add(game)
    db.session.flush()
    
    # Add current user as player
    game_player = GamePlayer(game_id=game.id, user_id=user_id, player_order=0)
    db.session.add(game_player)
    
    db.session.commit()
    return jsonify({'success': True, 'game_id': game.id})
>>>>>>> 440508f301fc3d3ac477f2c85e3a6cdd4790c167

@app.route('/roll-dice', methods=['POST'])
@jwt_required()
def roll_dice():
<<<<<<< HEAD
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
=======
    user_id = get_jwt_identity()
    data = request.get_json()
    game_id = data.get('game_id')
    
    game = Game.query.get(game_id)
    if not game or not game.is_active:
        return jsonify({'error': 'No active game found'})
    
    # Get current player
    current_player = GamePlayer.query.filter_by(
        game_id=game_id, 
        user_id=user_id
    ).first()
    
    if not current_player:
        return jsonify({'error': 'You are not in this game'})
    
    dice = random.randint(1, 6)
    new_position = current_player.position + dice
    
    message = f"Rolled {dice}!"
    
    # Apply snakes and ladders
    if new_position in SNAKES:
        new_position = SNAKES[new_position]
        message += " Snake!"
    elif new_position in LADDERS:
        new_position = LADDERS[new_position]
        message += " Ladder!"
    
    current_player.position = new_position
    
    # Check for win condition
    if current_player.position >= 100:
        current_player.position = 100
        game.winner_id = current_player.user_id
        game.is_active = False
        message += " Winner!"
    
    db.session.commit()
    return jsonify({
        'dice': dice, 
        'position': current_player.position,
        'message': message,
        'winner': game.winner_id is not None
    })

@app.route('/game-state/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game_state(game_id):
    user_id = get_jwt_identity()
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'})
    
    # Check if user is in this game
    user_in_game = GamePlayer.query.filter_by(game_id=game_id, user_id=user_id).first()
    if not user_in_game:
        return jsonify({'error': 'Access denied'})
    
    players = GamePlayer.query.filter_by(game_id=game_id).order_by(GamePlayer.player_order).all()
    positions = {player.user.username: player.position for player in players}
    
    return jsonify({
        'positions': positions,
        'isActive': game.is_active,
        'winner': User.query.get(game.winner_id).username if game.winner_id else None
>>>>>>> 440508f301fc3d3ac477f2c85e3a6cdd4790c167
    })

if __name__ == '__main__':
    app.run(debug=True)