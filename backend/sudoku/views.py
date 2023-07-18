from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Your game board
game_board = [
    [None, 3, None, 1, 5, 2],
    [None, 1, None, 4, None, 3],
    [5, None, None, None, 1, 4],
    [1, None, None, 6, None, None],
    [3, 2, 1, None, 4, 6],
    [None, None, None, None, None, 1]
]

def get_game_board(request):
    return JsonResponse({'game_board': game_board})

@csrf_exempt
def make_move(request):
    # Parse the request body
    data = json.loads(request.body)

    # Get the player's move from the request
    row = data['row']
    col = data['col']
    value = data['value']

    # Update the game board with the player's move
    game_board[row][col] = value

    # Here you would have your AI make a move and update the game board
    i, j, k = compute_best_move_with_ai(game_board)
    game_board[i][j] = k

    return JsonResponse({'game_board': game_board})

def compute_best_move_with_ai(game_board):
    # naive ai
    return (0, 0, 0)
