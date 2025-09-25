from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, User, Game, GamePlayer
import random

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# Snakes and Ladders positions
SNAKES_LADDERS = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78,  # Snakes
    1: 38, 4: 14, 9: 21, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100  # Ladders
}

@app.before_first_request
def create_tables():
    db.create_all()

# Authentication Routes
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
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Game Logic Routes
@app.route('/start-game', methods=['POST'])
@jwt_required()
def start_game():
    user_id = get_jwt_identity()
    
    # Create new game
    game = Game()
    db.session.add(game)
    db.session.flush()  # Get game ID
    
    # Add player to game
    player = GamePlayer(game_id=game.id, user_id=user_id, position=0, player_order=0)
    db.session.add(player)
    db.session.commit()
    
    return jsonify({
        'game_id': game.id,
        'message': 'Game started successfully'
    })

@app.route('/roll-dice', methods=['POST'])
@jwt_required()
def roll_dice():
    user_id = get_jwt_identity()
    data = request.get_json()
    game_id = data.get('game_id')
    
    # Get current game and player
    game = Game.query.get(game_id)
    player = GamePlayer.query.filter_by(game_id=game_id, user_id=user_id).first()
    
    if not game or not player or game.winner_id:
        return jsonify({'error': 'Invalid game or game finished'}), 400
    
    # Roll dice
    dice_roll = random.randint(1, 6)
    new_position = player.position + dice_roll
    
    # Check if player wins
    if new_position >= 100:
        new_position = 100
        game.winner_id = user_id
        game.is_active = False
    
    # Apply snakes and ladders
    final_position = SNAKES_LADDERS.get(new_position, new_position)
    player.position = final_position
    
    db.session.commit()
    
    result = {
        'dice_roll': dice_roll,
        'new_position': final_position,
        'message': ''
    }
    
    if new_position in SNAKES_LADDERS:
        if SNAKES_LADDERS[new_position] < new_position:
            result['message'] = 'Snake! 🐍'
        else:
            result['message'] = 'Ladder! 🪜'
    
    if game.winner_id:
        result['message'] = 'Winner! 🎉'
        result['winner'] = True
    
    return jsonify(result)

@app.route('/game-state/<int:game_id>', methods=['GET'])
@jwt_required()
def game_state(game_id):
    user_id = get_jwt_identity()
    
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    # Check if user is in this game
    player = GamePlayer.query.filter_by(game_id=game_id, user_id=user_id).first()
    if not player:
        return jsonify({'error': 'Not authorized for this game'}), 403
    
    players = GamePlayer.query.filter_by(game_id=game_id).all()
    
    return jsonify({
        'game_id': game.id,
        'current_turn': game.current_turn,
        'winner_id': game.winner_id,
        'is_active': game.is_active,
        'players': [{
            'user_id': p.user_id,
            'username': p.user.username,
            'position': p.position,
            'player_order': p.player_order
        } for p in players]
    })

if __name__ == '__main__':
    app.run(debug=True)