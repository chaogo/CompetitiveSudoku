from .move import Move, TabooMove
from .board import SudokuBoard, print_board
from typing import List, Union
from threading import Event

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

# with human player(s) 
class GameStateHuman(GameState): 
    def __init__(self,
                 initial_board: SudokuBoard,
                 board: SudokuBoard,
                 taboo_moves: List[TabooMove],
                 moves: List[Union[Move, TabooMove]],
                 scores: List[int],
                 current_player: int = 1):
        """
        Inherits from GameState and adds current_player and additional methods.
        """
        super().__init__(initial_board, board, taboo_moves, moves, scores)
        self.current_player = current_player
        self.current_player_is_ai = False
        self.move_event = Event()
        self.current_move = Move(0, 0, 0)

    def switch_turns(self):
        """Switches the current player between 1 and 2."""
        self.current_player = 3 - self.current_player
        self.current_player_is_ai = not self.current_player_is_ai

    def is_game_over(self):
        # Check for game termination conditions
        return self.board.squares.count(SudokuBoard.empty) == 0 
        # TODO time limit reached | taboo moves made

    def wait_for_move(self):
        if self.current_player_is_ai: 
            self.ask_ai_move()
        else: 
            self.ask_human_move()
        return self.current_move
    
    def ask_human_move(self):
        self.move_event.wait()
        self.move_event.clear()

    def ask_ai_move(self):
        import requests
        import json

        # Define the URL and the payload
        url = "http://127.0.0.1:8001/aiMakeMove"

        payload = {
            "game_board": self.board.__str__().strip(),
            "ai_player": "minimax_player",
            "time_limit": 1
        }
        # Make the POST request
        move = requests.post(url, json=payload).json()
        self.current_move = Move(move['row'], move['col'], move['val'])

    def add_move(self, move: Move):
        self.current_move = move
        self.move_event.set()

    def make_move(self):
        if self.current_move == Move(0, 0, 0): return
        move = self.current_move
        self.board.put(move.i, move.j, move.value)
        print_board(self.board)
        self.current_move = Move(0, 0, 0) # reset current move needed?
        # TODO calculate scores as well
        # TODO validate move

    def validate_move(self, move: Move) -> bool:
        # TODO Check if the move comes from current player
        # TODO Check if the move is taboo move
        return True
