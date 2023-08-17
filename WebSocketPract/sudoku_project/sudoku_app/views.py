from django.http import JsonResponse
from .models import SudokuGame


def create_game(request):
    game = SudokuGame.objects.create(player1=request.user)
    return JsonResponse({'game_id': game.id})


def get_game_state(request, game_id):
    game = SudokuGame.objects.get(pk=game_id)
    return JsonResponse({'current_state': game.current_state})


def join_game(request, game_id):
    game = SudokuGame.objects.get(pk=game_id)

    if game.status != 'waiting':
        return JsonResponse({'error': 'Game is not available for joining or does not exist.'}, status=400)

    game.player2 = request.user
    game.status = 'ready'
    game.save()

    return JsonResponse({'message': 'Successfully joined the game!'})
