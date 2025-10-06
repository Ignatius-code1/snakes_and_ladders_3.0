from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Model 1: User
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One-to-many: User can have many games
    games = db.relationship('Game', backref='creator', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Model 2: Game
class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, active, finished
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Model 3: GamePlayer (Many-to-many with extra attributes)
class GamePlayer(db.Model):
    __tablename__ = 'game_players'
    
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Extra attributes (required for Phase 4)
    position = db.Column(db.Integer, default=0)
    player_order = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, default=0)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    game = db.relationship('Game', backref='players')
    user = db.relationship('User', backref='game_participations')