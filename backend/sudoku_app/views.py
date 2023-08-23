from django.http import JsonResponse
from .models import SudokuGame
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def create_game(request):
    game = SudokuGame.objects.create(player1=request.user)
    return redirect('start_game', game_id=game.id)

@login_required
def choose_game(request):
    return render(request, 'sudoku_app/choose_game.html')


def get_game_state(request, game_id):
    game = SudokuGame.objects.get(pk=game_id)
    return JsonResponse({'current_state': game.current_state})

def join_game_view(request):
    return redirect('join_game', game_id=request.GET.get('game_id'))


def join_game(request, game_id):
    game = SudokuGame.objects.get(pk=game_id)

    if game.status != 'waiting':
        return JsonResponse({'error': 'Game is not available for joining or does not exist.'}, status=400)

    game.player2 = request.user
    game.status = 'ready'
    game.save()

    return redirect('start_game', game_id=game_id)

def start_game(request, game_id):
    return render(request, 'sudoku_app/start_game.html', {'game_id': game_id})
