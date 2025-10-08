from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, Game, GamePlayer
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['*'])
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

@app.route('/start-game', methods=['POST'])
@jwt_required()
def start_game():
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

@app.route('/roll-dice', methods=['POST'])
@jwt_required()
def roll_dice():
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
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)