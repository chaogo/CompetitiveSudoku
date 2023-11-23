import multiprocessing
import time
import copy
from typing import List
from game_controller.game_state import GameState, SudokuBoard
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
      ai_player.best_move[0] = 0
      ai_player.best_move[1] = 0
      ai_player.best_move[2] = 0
      try:
        process = multiprocessing.Process(target=ai_player.compute_best_move, args=(game_state,))
        process.start()
        time.sleep(time_limit)
        lock.acquire()
        process.terminate()
        lock.release()
      except Exception as err:
        print('Error: an exception occurred.\n', err)
      
      return ai_player.best_move
