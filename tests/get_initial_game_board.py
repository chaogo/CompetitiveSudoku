import sys
sys.path.append('/Users/chao/Desktop/Projects/CompetitiveSudoku')
from game_controller import get_initial_sudoku_board, print_board
sudokuboard = get_initial_sudoku_board()
print(sudokuboard)
print(print_board(sudokuboard))
