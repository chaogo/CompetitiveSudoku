import re
from game_controller.utils import Move, solve_sudoku
from game_controller.game_state import GameState
from ai.sudokuai import SudokuAI
import platform

class SudokuAI(SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()
        self.solve_sudoku_path = 'bin\\solve_sudoku.exe' if platform.system() == 'Windows' else '.././game_controller/bin/solve_sudoku'  # N.B. this path is set from outside

    # Uses solve_sudoku to compute a greedy move.
    def compute_best_move(self, game_state: GameState) -> None:
        board = game_state.board
        board_text = str(board)
        options = '--greedy'
        taboo_moves = ' '.join(f'{move.i} {move.j} {move.value}' for move in game_state.taboo_moves)
        if taboo_moves:
            options += f' --taboo="{taboo_moves}"'
        output = solve_sudoku(self.solve_sudoku_path, board_text, options)
        m = re.search(r"Generated move \((\d+),(\d+)\)", output)
        if not m:
            raise RuntimeError('Could not generate a greedy move:\n' + output)
        k = int(m.group(1))
        value = int(m.group(2))
        i, j = board.f2rc(k)
        self.propose_move(Move(i, j, value))
