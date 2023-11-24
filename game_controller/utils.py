from typing import Tuple
import os
from pathlib import Path
import tempfile

class Move(object):
    """A Move is a tuple (i, j, value) that represents the action board.put(i, j, value) for a given
    sudoku configuration board."""

    def __init__(self, i: int, j: int, value: int):
        """
        Constructs a move.
        @param i: A row value in the range [0, ..., N)
        @param j: A column value in the range [0, ..., N)
        @param value: A value in the range [1, ..., N]
        """
        self.i = i
        self.j = j
        self.value = value

    def __str__(self):
        return f'({self.i},{self.j}) -> {self.value}'

    def __eq__(self, other):
        return (self.i, self.j, self.value) == (other.i, other.j, other.value)


class TabooMove(Move):
    """A TabooMove is a Move that was flagged as illegal by the sudoku oracle. In other words, the execution of such a
    move would cause the sudoku to become unsolvable.
    """

    """
    Constructs a taboo move.
    @param i: A row value in the range [0, ..., N)
    @param j: A column value in the range [0, ..., N)
    @param value: A value in the range [1, ..., N]
    """
    def __init__(self, i: int, j: int, value: int):
        super().__init__(i, j, value)

class SudokuBoard(object):
    """
    A simple board class for Sudoku. It supports arbitrary rectangular regions.
    """

    empty = 0  # Empty squares contain the value SudokuBoard.empty

    def __init__(self, m: int = 3, n: int = 3):
        """
        Constructs an empty Sudoku with regions of size m x n.
        @param m: The number of rows in a region.
        @param n: The number of columns in a region.
        """
        N = m * n
        self.m = m
        self.n = n
        self.N = N     # N = m * n, numbers are in the range [1, ..., N]
        self.squares = [SudokuBoard.empty] * (N * N)  # The N*N squares of the board

    def rc2f(self, i: int, j: int):
        """
        Converts row/column coordinates to the corresponding index in the board array.
        @param i: A row value in the range [0, ..., N)
        @param j: A column value in the range [0, ..., N)
        @return: The corresponding index k in the board array
        """
        N = self.N
        return N * i + j

    def f2rc(self, k: int) -> Tuple[int, int]:
        """
        Converts an index in the board array to the corresponding row/column coordinates.
        @param k: A value in the range [0, ..., N * N)
        @return: The corresponding row/column coordinates
        """
        N = self.N
        i = k // N
        j = k % N
        return i, j

    def put(self, i: int, j: int, value: int) -> None:
        """
        Puts the given value on the square with coordinates (i, j).
        @param i: A row value in the range [0, ..., N)
        @param j: A column value in the range [0, ..., N)
        @param value: A value in the range [1, ..., N]
        """
        k = self.rc2f(i, j)
        self.squares[k] = value

    def get(self, i: int, j: int):
        """
        Gets the value of the square with coordinates (i, j).
        @param i: A row value in the range [0, ..., N)
        @param j: A column value in the range [0, ..., N)
        @return: The value of the square.
        """
        k = self.rc2f(i, j)
        return self.squares[k]

    def region_width(self):
        """
        Gets the number of columns in a region.
        @return: The number of columns in a region.
        """
        return self.n

    def region_height(self):
        """
        Gets the number of rows in a region.
        @return: The number of rows in a region.
        """
        return self.m

    def board_width(self):
        """
        Gets the number of columns of the board.
        @return: The number of columns of the board.
        """
        return self.N

    def board_height(self):
        """
        Gets the number of rows of the board.
        @return: The number of rows of the board.
        """
        return self.N

    def __str__(self) -> str:
        """
        Prints the board in a simple textual format. The first line contains the values m and n. Then the contents of
        the rows are printed as space separated lists, where a dot '.' is used to represent an empty square.
        @return: The generated string.
        """
        import io

        m = self.m
        n = self.n
        N = self.N
        out = io.StringIO()

        def print_square(i, j):
            value = self.get(i, j)
            s = '   .' if value == 0 else f'{value:>4}'
            out.write(s)

        out.write(f'{m} {n}\n')
        for i in range(N):
            for j in range(N):
                print_square(i, j)
            out.write('\n')
        return out.getvalue()
    
def load_sudoku_from_text(text: str) -> SudokuBoard:
    """
    Loads a sudoku board from a string, in the same format as used by the SudokuBoard.__str__ function.
    @param text: A string representation of a sudoku board.
    @return: The generated Sudoku board.
    """
    words = text.split()
    if len(words) < 2:
        raise RuntimeError('The string does not contain a sudoku board')
    m = int(words[0])
    n = int(words[1])
    N = m * n
    if len(words) != N*N + 2:
        raise RuntimeError('The number of squares in the sudoku is incorrect.')
    result = SudokuBoard(m, n)
    N = result.N
    for k in range(N * N):
        s = words[k + 2]
        if s != '.':
            value = int(s)
            result.squares[k] = value
    return result

def print_board(board: SudokuBoard) -> str: 
    """print a sudoku board in a pretty way
    """
    import io

    m = board.m
    n = board.n
    N = board.N
    out = io.StringIO()

    def print_square(i, j):
        value = board.get(i, j)
        s = ' -' if value == 0 else f'{value:2}'
        return s

    for i in range(N):

        # open the grid
        if i == 0:
            out.write('  ')
            for j in range(N):
                out.write(f'   {j}  ')
            out.write('\n')
            for j in range(N):
                if j % n != 0:
                    out.write('╤═════')
                elif j != 0:
                    out.write('╦═════')
                else:
                    out.write('   ╔═════')
            out.write('╗\n')

        # separate regions horizontally
        if i % m == 0 and i != 0:
            for j in range(N):
                if j % n != 0:
                    out.write('╪═════')
                elif j != 0:
                    out.write('╬═════')
                else:
                    out.write('   ╠═════')
            out.write('║\n')

        # plot values
        out.write(f'{i:2} ')
        for j in range(N):
            symbol = print_square(i, j)
            if j % n != 0:
                out.write(f'│ {symbol}  ')
            else:
                out.write(f'║ {symbol}  ')
            if len(symbol) < 2:
                out.write(' ')
        out.write('║\n')

        # close the grid
        if i == N - 1:
            for j in range(N):
                if j % n != 0:
                    out.write('╧═════')
                elif j != 0:
                    out.write('╩═════')
                else:
                    out.write('   ╚═════')
            out.write('╝\n')

    return out.getvalue()


def execute_command(command: str) -> str:
    import subprocess
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as proc:
        output = proc.output
    return output.decode("utf-8").strip()


def solve_sudoku(solve_sudoku_path: str, board_text: str, options: str='') -> str:
    """
    Execute the solve_sudoku program.
    @param solve_sudoku_path: The location of the solve_sudoku executable.
    @param board_text: A string representation of a sudoku board.
    @param options: Additional command line options.
    @return: The output of solve_sudoku.
    """
    if not os.path.exists(solve_sudoku_path):
        raise RuntimeError(f'No oracle found at location "{solve_sudoku_path}"')
    filename = tempfile.NamedTemporaryFile(prefix='solve_sudoku_').name
    Path(filename).write_text(board_text)
    command = f'{solve_sudoku_path} {filename} {options}'
    return execute_command(command)