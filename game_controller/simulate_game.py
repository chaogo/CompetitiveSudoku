import copy
from .utils import SudokuBoard, load_sudoku_from_text
from .game_state import GameStateHuman
from .games import active_games
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .referee import referee

def simulate_game(game_id, board_text):
    initial_board = load_sudoku_from_text(board_text)
    game_state = GameStateHuman(initial_board, copy.deepcopy(initial_board), [], [], [0, 0])
    active_games[game_id] = game_state
    channel_layer = get_channel_layer()

    # Broadcast the initial game board
    async_to_sync(channel_layer.group_send)(
        f"sudoku_{game_id}",  # group name
        {
            'type': 'broadcast_message',
            'message': "Game Start!",
            'board': str(game_state.board)
        }
    )

    while not game_state.is_game_over():
        # Wait for a player move
        move = game_state.wait_for_move()

        # Process the move
        referee_message = ""
        if move:
            referee_message = referee(game_state, move) # meanwhile make move if feasible 
            # TODO calculate score
        else:
            # TODO Time limit reached, but no move was made
            pass

        # broadcast the gamestate
        async_to_sync(channel_layer.group_send)(
            f"sudoku_{game_id}",  # group name
            {
                'type': 'broadcast_message',
                'message': f"{referee_message}    score: {game_state.scores}", # f"{referee_message}\nPlayer{game_state.current_player}: it's your turn \n",
                'board': str(game_state.board)
            }
        )

        # switch turns
        game_state.switch_turns()

    # End the game and notify players
    del active_games[game_id]
