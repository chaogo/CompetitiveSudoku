import sys
import os
sys.path.append('/Users/chao/Desktop/fj/Projects/CompetitiveSudoku/CompetitiveSudoku')
import importlib
from flask import Flask, request, jsonify
from game_controller.utils import load_sudoku_from_text
from calculate_move import calculate_move


app = Flask(__name__)

@app.route('/aiMakeMove', methods=['POST'])
def make_move():
    # Extract game data from the JSON request
    json_data = request.json
    game_board = load_sudoku_from_text(json_data.get('game_board'))
    ai_player = importlib.import_module(json_data.get('ai_player') + '.sudokuai').SudokuAI()
    time_limit = float(json_data.get('time_limit'))

    # AI logic to decide the move
    move = calculate_move(game_board, ai_player, time_limit)

    return jsonify({"move": {"row": move[0], "col": move[1], "val": move[2]}})

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 8001))
    app.run(host=host, port=port, debug=True)
