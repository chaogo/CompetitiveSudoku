from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Your game board
game_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
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
    number = data['number']

    # Update the game board with the player's move
    game_board[row][col] = number

    # Here you would have your AI make a move and update the game board
    i, j, k = compute_best_move_with_ai(game_board)
    game_board[i][j] = k

    return JsonResponse({'row': i, 'col': j, 'number': k})

def compute_best_move_with_ai(game_board):
    # naive ai
    return (1, 1, -1)
