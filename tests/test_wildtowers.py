import math
from io import StringIO

from vlo.wildtowers import wild_towers, process_data, make_matrix_from_0_and_1, make_matrix_from_dot_and_letter_o, \
    generate_combinations, solve_brute_force, allowable_positions, validate_combination


def test_can_make_matrix_from_0_1():
    assert make_matrix_from_0_and_1('') == []
    assert make_matrix_from_0_and_1('Hello') == []
    assert make_matrix_from_0_and_1('0') == [[0]]
    assert make_matrix_from_0_and_1('1') == [[1]]
    assert make_matrix_from_0_and_1('0110') == [[0, 1], [1, 0]]
    assert make_matrix_from_0_and_1("""0
    1 end of the first row
    1
    0 end of the second / final row
    """) == [[0, 1], [1, 0]]


def test_can_make_matrix_from_dot_o():
    assert make_matrix_from_dot_and_letter_o('') == []
    assert make_matrix_from_dot_and_letter_o('Hello') == [[0]]
    assert make_matrix_from_dot_and_letter_o('o') == [[0]]
    assert make_matrix_from_dot_and_letter_o('.') == [[1]]
    assert make_matrix_from_dot_and_letter_o('o..o') == [[0, 1], [1, 0]]


def test_can_solve_brute_force():
    assert solve_brute_force([]) == 0


def test_can_validate_combinations():
    assert not validate_combination(((0, 0), (1, 0), (2, 1)))
    assert validate_combination(((0, 0), (1, 1), (2, 2)))


def test_can_generate_combinations():
    assert list(generate_combinations([])) == []
    assert list(generate_combinations([[0]])) == []
    assert list(generate_combinations([[1]])) == [((0, 0),)]
    assert list(generate_combinations([[1, 1],
                                       [0, 1]])) == [((0, 0), (1, 1)),
                                                     ((0, 1), (1, 1))]
    assert list(generate_combinations([[1, 1, 0],
                                       [1, 0, 1],
                                       [0, 1, 1]])) == [
        ((0, 0), (1, 0), (2, 1)),
        ((0, 0), (1, 0), (2, 2)),
        ((0, 0), (1, 2), (2, 1)),
        ((0, 0), (1, 2), (2, 2)),
        ((0, 1), (1, 0), (2, 1)),
        ((0, 1), (1, 0), (2, 2)),
        ((0, 1), (1, 2), (2, 1)),
        ((0, 1), (1, 2), (2, 2))]
    assert list(generate_combinations([[1, 1],
                                       [0, 0]])) == []


def test_can_get_allowable_positions():
    assert list(allowable_positions([])) == [[]]
    assert list(allowable_positions([[0]])) == [[]]
    assert list(allowable_positions([[1]])) == [[(0, 0)]]
    assert list(allowable_positions([[1, 0],
                                     [0, 1]])) == [[(0, 0)], [(1, 1)]]
    assert list(allowable_positions([[1, 1],
                                     [0, 1]])) == \
           [[(0, 0), (0, 1)], [(1, 1)]]


def test_can_solve_empty():
    assert wild_towers() == 0


def test_can_solve_1x1_square():
    assert wild_towers('1') == 1


def test_can_solve_1x1_square_with_hole():
    assert wild_towers('0') == 0


def test_can_solve_2x2_square():
    assert wild_towers('1111') == 2


def test_can_solve_2x2_square_with_row_holes():
    assert wild_towers('0011') == 0


def test_can_solve_empty_squares():
    for i in range(1, 10):
        assert wild_towers('0' * (i * i)) == 0


def test_can_solve_half_empty_squares():
    print()
    for size in range(1, 11):
        board0 = ''
        board1 = ''
        for position in range(size):
            if position % 2:
                gen0 = ('01' * size)[:size]
                gen1 = ('10' * size)[:size]
            else:
                gen0 = ('10' * size)[:size]
                gen1 = ('01' * size)[:size]
            board0 += gen0
            board1 += gen1
        print(len(board0), wild_towers(board0), wild_towers(board1))


def test_can_solve_full_squares():
    for i in range(1, 9):
        assert wild_towers('1' * (i * i)) == math.factorial(i)

def test_can_solve_5x5_squares():
    print()
    size = 6
    assert wild_towers('1' * (size*size), print_result=True) == math.factorial(size)



def test_can_process_data():
    input = """1
3
..o
.o.
o..    
    """
    out = StringIO()
    inp = StringIO(input)
    process_data(inp, out)
    text = out.getvalue()[:-1]
    assert text == '2'
