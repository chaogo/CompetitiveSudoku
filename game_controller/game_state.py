from game_controller.utils import Move, SudokuBoard, TabooMove, print_board
from typing import List, Union
from threading import Event

class GameState(object):
    def __init__(self,
                 initial_board: SudokuBoard,
                 board: SudokuBoard,
                 taboo_moves: List[TabooMove],
                 moves: List[Union[Move, TabooMove]],
                 scores: List[int],
                 current_player: int = 1):
        """
        @param initial_board: A sudoku board. It contains the start position of a game.
        @param board: A sudoku board. It contains the current position of a game.
        @param taboo_moves: A list of taboo moves. Moves in this list cannot be played.
        @param moves: The history of a sudoku game, starting in initial_board. The
        history includes taboo moves.
        @param scores: The current scores of the first and the second player.
        """
        self.initial_board = initial_board
        self.board = board
        self.taboo_moves = taboo_moves
        self.moves = moves
        self.scores = scores
        self.current_player = current_player
        # self.move_event = Event() # would impact the ai's multiprocessing
        self.current_move = None

    def switch_turns(self):
        """Gives the index of the current player (1 or 2).
        @return The index of the current player.
        """
        self.current_player = 3 - self.current_player
    
    def is_game_over(self):
        # Check for game termination conditions
        return self.board.squares.count(SudokuBoard.empty) == 0 
        # TODO time limit reached | taboo moves made

    def wait_for_move(self):
        self.move_event.wait()
        self.move_event.clear()
        return self.current_move

    def add_move(self, move: Move):
        self.current_move = move
        self.move_event.set()

    def make_move(self):
        if not self.current_move: return
        move = self.current_move
        self.board.put(move.i, move.j, move.value)
        print_board(self.board)
        self.current_move = None # reset current move needed?
        # TODO calculate scores as well
        # TODO validate move

    def validate_move(self, move: Move) -> bool:
        # TODO Check if the move comes from current player
        # TODO Check if the move is taboo move
        return True
    
    def __str__(self):
        import io
        out = io.StringIO()
        out.write(print_board(self.board))
        out.write(f'Score: {self.scores[0]} - {self.scores[1]}')
        return out.getvalue()