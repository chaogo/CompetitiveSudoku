from game_controller.utils import Move, TabooMove


def referee(best_move):
  if best_move != Move(0, 0, 0):
      if TabooMove(i, j, value) in game_state.taboo_moves:
          print(f'Error: {best_move} is a taboo move. Player {3-player_number} wins the game.')
          return
      board_text = str(game_state.board)
      options = f'--move "{game_state.board.rc2f(i, j)} {value}"'
      output = solve_sudoku(solve_sudoku_path, board_text, options)
      if 'Invalid move' in output:
          print(f'Error: {best_move} is not a valid move. Player {3-player_number} wins the game.')
          return
      if 'Illegal move' in output:
          print(f'Error: {best_move} is not a legal move. Player {3-player_number} wins the game.')
          return
      if 'has no solution' in output:
          print(f'The sudoku has no solution after the move {best_move}.')
          player_score = 0
          game_state.moves.append(TabooMove(i, j, value))
          game_state.taboo_moves.append(TabooMove(i, j, value))
      if 'The score is' in output:
          match = re.search(r'The score is ([-\d]+)', output)
          if match:
              player_score = int(match.group(1))
              game_state.board.put(i, j, value)
              game_state.moves.append(best_move)
              move_number = move_number + 1
          else:
              raise RuntimeError(f'Unexpected output of sudoku solver: "{output}".')
  else:
      print(f'No move was supplied. Player {3-player_number} wins the game.')
      return
  game_state.scores[player_number-1] = game_state.scores[player_number-1] + player_score
  print(f'Reward: {player_score}')
  print(game_state)

  if game_state.scores[0] > game_state.scores[1]:
      print('Player 1 wins the game.')
  elif game_state.scores[0] == game_state.scores[1]:
      print('The game ends in a draw.')
  elif game_state.scores[0] < game_state.scores[1]:
      print('Player 2 wins the game.')