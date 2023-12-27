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