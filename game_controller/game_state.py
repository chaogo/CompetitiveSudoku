from .player import Player
from .move import Move, TabooMove
from .board import SudokuBoard, print_board
from .games import active_games
from .utils import solve_sudoku
from typing import List, Union
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import platform
import re

class GameState(object):
    def __init__(self,
                 initial_board: SudokuBoard,
                 board: SudokuBoard,
                 taboo_moves: List[TabooMove],
                 moves: List[Union[Move, TabooMove]],
                 scores: List[int]):
        """
        @param initial_board: A sudoku board. It contains the start position of a game.
        @param board: A sudoku board. It contains the current position of a game.
        @param taboo_moves: A list of taboo moves. Moves in this list cannot be played.
        @param moves: The history of a sudoku game, starting in initial_board.
        @param scores: The current scores of the first and the second player.
        """
        self.initial_board = initial_board
        self.board = board
        self.taboo_moves = taboo_moves
        self.moves = moves
        self.scores = scores

    def __str__(self):
        import io
        out = io.StringIO()
        out.write(print_board(self.board))
        out.write(f'Score: {self.scores[0]} - {self.scores[1]}')
        return out.getvalue()

class GameStatePlus(GameState): 
    def __init__(self,
                 initial_board: SudokuBoard,
                 board: SudokuBoard,
                 taboo_moves: List[TabooMove],
                 moves: List[Union[Move, TabooMove]],
                 scores: List[int],
                 player1: Player,
                 player2: Player,
                 game_id: int,
                 is_game_over: bool = False):
        """
        Inherits from GameState, plus players, and functions to run the game
        """
        super().__init__(initial_board, board, taboo_moves, moves, scores)
        self.player1 = player1
        self.player2 = player2
        self.game_id = game_id
        self.is_game_over = is_game_over
        self.current_player = player1 # player1 by default makes the first move

    def switch_turns(self):
        self.current_player = self.player1 if self.current_player is self.player2 else self.player2

    def wait_for_move(self):
        return self.current_player.get_move(self.board)

    def broadcast_game_message(self, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"sudoku_{self.game_id}",  # group name
            {
                'type': 'broadcast_message',
                'message': message,
                'board': str(self.board)
            }
        )

    def simulate_game(self):
        # Broadcast the initial game board
        self.broadcast_game_message("Game Start!")

        while not self.is_game_over:
            # Wait for a player move
            move = self.wait_for_move()

            # Process the move
            referee_message = ""
            if move:
                self.is_game_over, referee_message = self.referee(move) # meanwhile make move if feasible 

            # broadcast the gamestate
            self.broadcast_game_message(f"{referee_message}    score: {self.scores}")

            # switch turns
            self.switch_turns()

        # Delete the game and end the thread naturally
        del active_games[self.game_id]

    def referee(self, current_move: Move) -> (bool, str):
        i, j, value = current_move.i, current_move.j, current_move.value
        player_number = self.current_player.number
        solve_sudoku_path = 'game_controller\\bin\\solve_sudoku.exe' if platform.system() == 'Windows' else 'game_controller/bin/solve_sudoku'
        mes = f'current move: {current_move}\n'
        if current_move == Move(0, 0, 0):
            return True, f'No move was supplied. Player {3-player_number} wins the game.'
        else:
            if TabooMove(i, j, value) in self.taboo_moves:
                return True, f'Error: {current_move} is a taboo move. Player {3-player_number} wins the game.'
            
            board_text = str(self.board)
            options = f'--move "{self.board.rc2f(i, j)} {value}"'
            output = solve_sudoku(solve_sudoku_path, board_text, options)
            if 'Invalid move' in output:
                return True, f'Error: {current_move} is not a valid move. Player {3-player_number} wins the game.'
            if 'Illegal move' in output:
                return True, f'Error: {current_move} is not a legal move. Player {3-player_number} wins the game.'
            if 'has no solution' in output:
                self.moves.append(TabooMove(i, j, value))
                self.taboo_moves.append(TabooMove(i, j, value))
                return False, f'The sudoku has no solution after the move {current_move}. Move is canceled and No reward is earned'
            if 'The score is' in output:
                match = re.search(r'The score is ([-\d]+)', output)
                if not match:
                    raise RuntimeError(f'Unexpected output of sudoku solver: "{output}".')
                else:
                    player_score = int(match.group(1))
                    self.board.put(i, j, value)
                    self.moves.append(current_move)
                    self.scores[player_number-1] = self.scores[player_number-1] + player_score
                    mes += f'Reward: {player_score}\n'

        # check if the game board gets filled up after current move
        if self.board.squares.count(SudokuBoard.empty) != 0:
            return False, mes
        
        if self.scores[0] > self.scores[1]:
            mes += '\nPlayer 1 wins the game.'
        elif self.scores[0] == self.scores[1]:
            mes += '\nThe game ends in a draw.'
        elif self.scores[0] < self.scores[1]:
            mes += '\nPlayer 2 wins the game.'
        return True, mes