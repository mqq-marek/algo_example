import math


def make_matrix(board):
    """Read board as a sequence of chars 0 and 1 and treat them as board.
    Char 0 means hole and placing rock is not possible.
    Char 1 means normal place when we can place rook/tower
    Character other than 0 and 1 are skipped.
    Result is matrix of rows with 0/1 char.
    """
    assert isinstance(board, str)
    filtered_board = [ch for ch in board if ch in "01"]
    total = len(filtered_board)
    size = int(math.sqrt(total))
    assert size * size == total
    rows = [filtered_board[row * size:(row + 1) * size]
            for row in range(size)]
    matrix = [[ch for ch in row]
              for row in rows
              ]
    return matrix


class TowerSolver:

    def __init__(self, board):
        # Convert board to matrix
        self.matrix = make_matrix(board)
        # Make empty hash table/dictionary for storing temporary results
        self.mapper = {}

    def solver(self):
        return self.solve([ndx for ndx in range(len(self.matrix))])

    def solve(self, columns):
        # list of columns determine matrix size for solve - at start we have all columns - full matrix size
        size = len(columns)
        if size == 0:
            return 0
        if size == 1:
            return int(self.matrix[0][columns[0]])
        # For every matrix for solve keep its result under key <col1>_<col2>_..._<coln>
        map_key = '_'.join(map(str, columns))
        result = self.mapper.get(map_key)
        if result is None:
            # cCompute result if not in mapper
            result = 0
            for column in columns:
                if self.matrix[size - 1][column]:
                    result += self.solve([col for col in columns if col != column])
            self.mapper[map_key] = result
        return result


def solve_loop_recursive(matrix):
    # recursive / slower solution without memorisation (storing partial results)
    # in addition for every recursive call new matrix is build which is time consuming
    if len(matrix) == 1:
        return int(matrix[0][0])

    left_col = [row[0] for row in matrix]
    return sum([solve_loop_recursive([row[1:]
                                      for ndx, row in enumerate(matrix)
                                      if ndx != index])
                for index, value in enumerate(left_col) if value

                ])


def wild_towers(board=''):
    matrix = make_matrix(board)
    # r1 = solve_loop_recursive(matrix)
    t = TowerSolver(board)
    r2 = t.solver()
    r1 = r2
    if r1 != r2:
        print(f'Fail solve {matrix} and get {r1} & {r2}')
    return r1
