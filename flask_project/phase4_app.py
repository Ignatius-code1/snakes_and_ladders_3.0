from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from phase4_models import db, User, Game, GamePlayer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phase4_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

# AUTH ROUTES
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'access_token': token, 'user_id': user.id})
    return jsonify({'error': 'Invalid credentials'}), 401

# FULL CRUD FOR GAMES
@app.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    games = Game.query.all()
    return jsonify([{
        'id': g.id, 'name': g.name, 'status': g.status,
        'created_by': g.created_by, 'winner_id': g.winner_id
    } for g in games])

@app.route('/games', methods=['POST'])
@jwt_required()
def create_game():
    user_id = get_jwt_identity()
    data = request.get_json()
    game = Game(name=data['name'], created_by=user_id)
    db.session.add(game)
    db.session.flush()
    
    # Add creator as first player
    player = GamePlayer(game_id=game.id, user_id=user_id, player_order=1)
    db.session.add(player)
    db.session.commit()
    return jsonify({'id': game.id, 'name': game.name}), 201

@app.route('/games/<int:game_id>', methods=['PATCH'])
@jwt_required()
def update_game(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.get_json()
    if 'name' in data:
        game.name = data['name']
    if 'status' in data:
        game.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Game updated'})

@app.route('/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted'})

# CRUD FOR PLAYERS
@app.route('/games/<int:game_id>/players', methods=['GET'])
def get_players(game_id):
    players = GamePlayer.query.filter_by(game_id=game_id).all()
    return jsonify([{
        'id': p.id, 'user_id': p.user_id, 'position': p.position,
        'player_order': p.player_order, 'score': p.score
    } for p in players])

@app.route('/games/<int:game_id>/players', methods=['POST'])
@jwt_required()
def join_game(game_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    player = GamePlayer(
        game_id=game_id, 
        user_id=user_id, 
        player_order=data['player_order']
    )
    db.session.add(player)
    db.session.commit()
    return jsonify({'message': 'Joined game'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)