import importlib
import multiprocessing
import time
import copy
from typing import List
from game_controller.game_state import GameState
from game_controller.utils import load_sudoku_from_text, SudokuBoard
from sudokuai import SudokuAI


def calculate_move(game_board: SudokuBoard, ai_player: SudokuAI,  time_limit: float = 0.5) -> List[int]:
    """
    AI calculates the best move on current game board.
    @param game_board: The current position of the game.
    @param ai_player: The AI player
    @param calculation_time: The amount of time in seconds for computing the best move.
    """

    N = game_board.N

    game_state = GameState(game_board, copy.deepcopy(game_board), [], [], [0, 0])
    print(game_state)

    with multiprocessing.Manager() as manager:
      # use a lock to protect assignments to best_move
      lock = multiprocessing.Lock()
      ai_player.lock = lock

      # use shared variables to store the best move
      ai_player.best_move = manager.list([0, 0, 0])
      try:
        process = multiprocessing.Process(target=ai_player.compute_best_move, args=(game_state,))
        process.start()
        time.sleep(time_limit)
        lock.acquire()
        process.terminate()
        lock.release()
      except Exception as err:
        print('Error: an exception occurred.\n', err)
      
      i, j, value = ai_player.best_move
      return [i, j, value]


if __name__ == '__main__':
  board_text = '''2 2
      1   2   3   4
      3   4   .   2
      2   1   .   3
      .   .   .   1
  '''
  game_board = load_sudoku_from_text(board_text)
  ai_player = importlib.import_module('minimax_player.sudokuai').SudokuAI()
  time_limit = 1.0
  calculate_move(game_board, ai_player, time_limit)