from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

game_state = {
    'players': [],
    'positions': {},
    'currentPlayer': 0
}

@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.get_json()
    game_state['players'] = data['players']
    game_state['positions'] = {player: 0 for player in data['players']}
    game_state['currentPlayer'] = 0
    return jsonify({'success': True})

@app.route('/roll-dice', methods=['POST'])
def roll_dice():
    if not game_state['players']:
        return jsonify({'error': 'No game started'})
    
    dice = random.randint(1, 6)
    current_player = game_state['players'][game_state['currentPlayer']]
    game_state['positions'][current_player] += dice
    
    game_state['currentPlayer'] = (game_state['currentPlayer'] + 1) % len(game_state['players'])
    return jsonify({'dice': dice})

@app.route('/game-state', methods=['GET'])
def get_game_state():
    return jsonify({
        'currentPlayer': game_state['players'][game_state['currentPlayer']] if game_state['players'] else None,
        'positions': game_state['positions']
    })

if __name__ == '__main__':
    app.run(debug=True)