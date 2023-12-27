import platform
import re
from .move import Move, TabooMove
from .utils import solve_sudoku
from .game_state import GameStateHuman

def referee(game_state: GameStateHuman, current_move: Move):
    i, j, value = current_move.i, current_move.j, current_move.value
    player_number = game_state.current_player
    solve_sudoku_path = 'game_controller\\bin\\solve_sudoku.exe' if platform.system() == 'Windows' else 'game_controller/bin/solve_sudoku'
    res = f'current move: {current_move}\n'
    if current_move == Move(0, 0, 0):
        return f'No move was supplied. Player {3-player_number} wins the game.'
    else:
        if TabooMove(i, j, value) in game_state.taboo_moves:
            return f'Error: {current_move} is a taboo move. Player {3-player_number} wins the game.'
        
        board_text = str(game_state.board)
        options = f'--move "{game_state.board.rc2f(i, j)} {value}"'
        output = solve_sudoku(solve_sudoku_path, board_text, options)
        if 'Invalid move' in output:
            return f'Error: {current_move} is not a valid move. Player {3-player_number} wins the game.'
        if 'Illegal move' in output:
            return f'Error: {current_move} is not a legal move. Player {3-player_number} wins the game.'
        if 'has no solution' in output:
            game_state.moves.append(TabooMove(i, j, value))
            game_state.taboo_moves.append(TabooMove(i, j, value))
            return f'The sudoku has no solution after the move {current_move}. Move is canceled and No reward is earned'
        if 'The score is' in output:
            match = re.search(r'The score is ([-\d]+)', output)
            if not match:
                raise RuntimeError(f'Unexpected output of sudoku solver: "{output}".')
            else:
                player_score = int(match.group(1))
                game_state.board.put(i, j, value)
                game_state.moves.append(current_move)
                game_state.scores[player_number-1] = game_state.scores[player_number-1] + player_score
                res += f'Reward: {player_score}\n'

    if game_state.is_game_over():
        if game_state.scores[0] > game_state.scores[1]:
            res += '\nPlayer 1 wins the game.'
        elif game_state.scores[0] == game_state.scores[1]:
            res += '\nThe game ends in a draw.'
        elif game_state.scores[0] < game_state.scores[1]:
            res += '\nPlayer 2 wins the game.'
    return res