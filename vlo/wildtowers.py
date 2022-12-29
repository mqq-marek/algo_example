import itertools
import json
import math
from collections import defaultdict
from operator import itemgetter
from sys import stdin, stdout


def make_matrix_from_0_and_1(board):
    """Read board as a sequence of chars 0 and 1 and treat them as board.
    Char 0 means hole and placing rock is not possible.
    Char 1 means normal place when we can place rook/tower
    Character other than 0 and 1 are skipped.
    Amount of 0 and 1 chars must be square of integer (must form matrix)
    Result is matrix of rows with 0/1 int.
    """
    assert isinstance(board, str)
    filtered_board = [ch for ch in board if ch in "01"]     # remove chars not being 0 nor 1
    total = len(filtered_board)                             # count amount of 0's and 1's
    size = int(math.sqrt(total))                            # count integer square root
    assert size * size == total                             # verify that total is square of size
    # rows is filtered_board split into 'size' rows having 'size' chars
    rows = [filtered_board[row_index * size:(row_index + 1) * size]     # take next size chars
                                                                        # from filtered_board string
            for row_index in range(size)
            ]
    matrix = [[int(ch) for ch in row]                       # 'size' chars string of 0's and 1's converted
                                                            # into list of 0 and 1
              for row in rows
              ]
    return matrix


def make_matrix_from_dot_and_letter_o(board):
    """Read board as a sequence of chars 0 and 1 and treat them as board.
    Char o means hole and placing rock is not possible.
    Char . means normal place when we can place rook/tower
    Character other than . and o are skipped.
    Amount of . and o chars must be square of integer (must form matrix)
    Result is matrix of rows with 0/1 char.
    """
    assert isinstance(board, str)
    zero_one_board = board.replace('.', '1').replace('o', '0')
    return make_matrix_from_0_and_1(zero_one_board)


def solve_brute_force(matrix):
    """Solve by creating all possible figure combinations - once at every row - and
    validate if they all have coordinates which prevent rooks to be able to attack
    other rook in single move."""
    list_for_check = generate_combinations(matrix)
    result = sum(validate_combination(postions, matrix) for postions in list_for_check)
    return result


def generate_combinations(matrix):
    """Create all possible (brute-force) combination list where figures can be placed on board.
    EG. for matrix 11/01 create [((0, 0), (1, 1)), ((0, 1), (1, 1))].

    """
    # return itertools.combinations(range(len(matrix)), len(matrix))
    # return itertools.permutations(range(len(matrix)), len(matrix))
    return itertools.product(*allowable_positions(matrix))


def allowable_positions(matrix):
    """Based on board matrix generate for list of row list with all coordinates for squares when rook can be placed.
    EG. for matrix 11/01 create [[(0, 0), (0, 1)], [(1, 1)]]. """
    if matrix:
        positions = [
            [(row_ndx, col_ndx)
             for col_ndx, square in enumerate(row)
             if square == 1
             ]
            for row_ndx, row in enumerate(matrix)
        ]
        return positions
    return [[]]


def validate_combination(positions, matrix=None):
    """Validate if given list of rook positions is ok for rook that means that
    all row and all col coordinates are different."""
    row_coords,col_coords = zip(*positions)
    # depend on the way how positions are generated validate:
    # necessary if position is generated using: itertools.combinations(range(len(matrix)), len(matrix)) or
    # itertools.permutations(range(len(matrix)), len(matrix)) for skip positions when we have hole on some position
    if matrix and not all(matrix[row_ndx][col_ndx] == 1 for row_ndx, col_ndx in zip(row_coords, col_coords)):
        return False
    # verify that all row and col coords are unique so len(set(sequence)) = len(sequence)
    return len(set(row_coords)) == len(set(col_coords)) == len(positions)


def process_data(input, output):
    z = int(input.readline())
    for _ in range(z):
        n = int(input.readline())
        board = ''
        for _ in range(n):
            board += input.readline()
        matrix = make_matrix_from_dot_and_letter_o(board)
        result = wild_towers(matrix)
        output.write(str(result) + '\n')


class TowerSolver:

    def __init__(self, matrix):
        # Convert board to matrix
        self.matrix = matrix
        # Make empty hash table/dictionary for storing temporary results
        self.mapper = {}
        self.counter = defaultdict(int)

    def solver(self):
        return self.solve([ndx for ndx in range(len(self.matrix))])

    def solve(self, columns):
        # list of columns determine matrix size for solve - at start we have all columns - full matrix size
        size = len(columns)
        # For every matrix for solve keep its result under key <col1>_<col2>_..._<coln>
        map_key = '_'.join(map(str, columns))
        self.counter[map_key] += 1
        if size == 0:
            return 0
        if size == 1:
            return int(self.matrix[0][columns[0]])

        result = self.mapper.get(map_key)
        if result is None:
            # Compute result if not in mapper
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
    return sum([solve_loop_recursive([row[1:]                               # build matrix without first element in row
                                      for ndx, row in enumerate(matrix)
                                      if ndx != index])                     # for all rws except current index
                for index, value in enumerate(left_col)                     # for indexed values of left_col
                if value                                                    # when value is 1
                ])

# If DEBUG True verify results of all 3 methods - slow!
DEBUG = False


def wild_towers(board='', print_result=False):
    # Matrix example: [[1,0, 1], [1, 1, 1], [1, 0, 1]]
    matrix = []
    if isinstance(board, str):
        if '0' in board or '1' in board:
            matrix = make_matrix_from_0_and_1(board)
        else:
            matrix = make_matrix_from_dot_and_letter_o(board)
    elif isinstance(board, list):
        matrix = board

    t = TowerSolver(matrix)
    result = t.solver()
    if print_result:
        keys = sorted(t.counter, key=t.counter.get, reverse=False)
        for key in keys:
            print(f"{key}:{t.counter[key]}")
    if DEBUG:
        result_first = solve_brute_force((matrix))
        result_test = solve_loop_recursive(matrix)
        if not result == result_test == result_first:
            print(f'Fail solving {matrix} and get {result} & {result_test} & {result_first}')
    return result


if __name__ == "__main__":
    process_data(stdin, stdout)
