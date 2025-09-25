from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

# Supabase config
SUPABASE_URL = os.getenv('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'your-supabase-anon-key')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return jsonify({'message': 'Supabase Flask server running'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return jsonify({'message': 'User created', 'user': response.user.id}), 201
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
        return jsonify({'access_token': response.session.access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/games', methods=['GET'])
def get_games():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        supabase.auth.set_session(token, '')
        response = supabase.table('games').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/games', methods=['POST'])
def create_game():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        supabase.auth.set_session(token, '')
        user = supabase.auth.get_user(token)
        
        # Create game
        game_response = supabase.table('games').insert({}).execute()
        game_id = game_response.data[0]['id']
        
        # Add player to game
        supabase.table('game_players').insert({
            'game_id': game_id,
            'user_id': user.user.id,
            'player_order': 1
        }).execute()
        
        return jsonify({'game_id': game_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5001)