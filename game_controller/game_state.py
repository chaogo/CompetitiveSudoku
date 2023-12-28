from .player import Player
from .move import Move, TabooMove
from .board import SudokuBoard, print_board
from typing import List, Union

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
                 player2: Player):
        """
        Inherits from GameState, plus players
        """
        super().__init__(initial_board, board, taboo_moves, moves, scores)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1 # player1 by default makes the first move

    def switch_turns(self):
        self.current_player = self.player1 if self.current_player is self.player2 else self.player2

    def is_game_over(self):
        return self.board.squares.count(SudokuBoard.empty) == 0 

    def wait_for_move(self):
        return self.current_player.get_move(self.board)
