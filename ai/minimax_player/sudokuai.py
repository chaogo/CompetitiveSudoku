import random
import time
from game_controller.utils import GameState, Move, TabooMove, SudokuBoard
from ai.sudokuai import SudokuAI
import copy

class SudokuAI(SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

    # N.B. This is a very naive implementation.
    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N
        n = game_state.board.n
        m = game_state.board.m

        def calculate_move_score(board, i, j, value, maximizing):
            """"
            The evaluation function evaluates the score in the game that will be obtained by the proposed move (i,j,value)
            """
            # Add our hypothetical move to the current situation on the board
            board.put(i, j, value)

            # Create variables for each region that could be completed by a move (row, column, region)
            # Where 1 = filled and 0 = not filled. All initialized to 1.
            row = 1
            column = 1
            block = 1

            # CHECK ROW: loop through all k values in row i
            for k in range(N):
                # Check if we find an empty cell in row i column k
                if board.get(i, k) == SudokuBoard.empty:
                    row = 0
                    break

            # CHECK COLUMN: loop through all l values in column j
            for l in range(N):
                # Check if we find an empty cell in column j row l
                if board.get(l, j) == SudokuBoard.empty:
                    column = 0
                    break

            # CHECK BLOCK: Loop through rows (l) and columns (k) inside
            # Find the coordinates of the upper left corner of the block in which (i,j) is positioned
            block_position_verti = i // m * m
            block_position_hori = j // n * n

            for l in range(block_position_verti, block_position_verti + m):
                for k in range(block_position_hori, block_position_hori + n):
                    if board.get(l, k) == SudokuBoard.empty:
                        block = 0
                        break

            # the total score in the game earned with this move
            score = 0
            regions_filled = row + column + block
            if maximizing:
                # Calculate the total score in the game for current move and return the score
                if regions_filled == 0:
                    score = 0
                elif regions_filled == 1:
                    score = 1
                elif regions_filled == 2:
                    score = 3
                elif regions_filled == 3:
                    score = 7

            if not maximizing:
                # Calculate the negated total score in the game for current move of the opposition
                if regions_filled == 0:
                    score = 0
                elif regions_filled == 1:
                    score = -1
                elif regions_filled == 2:
                    score = -3
                elif regions_filled == 3:
                    score = -7

            return score

        """ Returns all legal moves given a board """
        def get_all_legal_moves(board):

            # Generate all moves that are possible
            possible_moves = [Move(i, j, value) for i in range(N) for j in range(N) for value in range(1, N + 1) if
                              board.get(i, j) == SudokuBoard.empty and not TabooMove(i, j,
                                                                                     value) in game_state.taboo_moves]
            # filter out illegal moves
            all_moves_legal = []

            for move in possible_moves:
                i = move.i
                j = move.j
                value = move.value
                legal = True

                # Check if value already in row
                for k in range(N):
                    if game_state.board.get(i, k) == value:
                        legal = False
                        break

                if legal:
                    # Check if value already in column
                    for l in range(N):
                        if board.get(l, j) == value:
                            legal = False
                            break

                if legal:
                    # Find the coordinates of the upper left corner of the block in which (i,j) is positioned
                    block_position_verti = i // m * m
                    block_position_hori = j // n * n

                    # Loop through rows (l) and columns (k) inside
                    for l in range(block_position_verti, block_position_verti + m):
                        for k in range(block_position_hori, block_position_hori + n):
                            if board.get(l, k) == value:
                                legal = False
                                break

                # If all checks are passed add the move to the list of legal moves
                if legal:
                    all_moves_legal.append(move)

            return all_moves_legal

        def minimax(board, depth, max_player):

            if depth == 0:
                return 0

            moves = get_all_legal_moves(board)
            if not moves:
                return 0

            if max_player:
                max_eval = -float('inf')
                for move in moves:
                    i, j, value = move.i, move.j, move.value
                    # moved when implementing calculate_move_score
                    cur_move_score = calculate_move_score(board, i, j, value, True)
                    # aggregate scores
                    eval = cur_move_score + minimax(board, depth-1, False)
                    max_eval = max(max_eval, eval)
                    # reset | pop move from board
                    board.put(i, j, 0)
                return max_eval

            else:
                min_eval = float('inf')
                for move in moves:
                    i, j, value = move.i, move.j, move.value
                    # moved when implementing calculate_move_score
                    cur_move_score = calculate_move_score(board, i, j, value, False)
                    # aggregate scores
                    eval = cur_move_score + minimax(board, depth-1, True)
                    min_eval = min(min_eval, eval)
                    # reset | pop move from board
                    board.put(i, j, 0)
                return min_eval

        #get board and set as initial best move, the first of legal moves
        board = game_state.board
        moves = get_all_legal_moves(board)
        best_move = moves[0]
        self.propose_move(best_move)

        for depth in range(1, 20):
            #print(depth, '\t')  # usually can search for less than 5 layers
            max_eval = -float('inf')
            for move in moves:
                i, j, value = move.i, move.j, move.value
                cur_move_score = calculate_move_score(board, i, j, value, True)
                eval = cur_move_score + minimax(board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                board.put(i, j, 0)
            self.propose_move(best_move)

#----------------------------#
# the order of playing matters for small-size game board, e.g. easy-2x2.txt
# compared with greedy_player, the minimax agent considers more turns, so it usually get fewer scores in the early stage, but overtake the opponent later
# the scores are very close when losing to greedy_player