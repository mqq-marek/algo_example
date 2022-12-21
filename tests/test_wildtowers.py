


import math

from vlo.wildtowers import wild_towers


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
        assert wild_towers('0'*(i * i)) == 0

def test_can_solve_half_empty_squares():
    print()
    for i in range(1, 21):
        board0 = ''
        board1 = ''
        for j in range(i):
            if j % 2:
                gen0 = ('01' * i)[:i]
                gen1 = ('10' * i)[:i]
            else:
                gen0 = ('10' * i)[:i]
                gen1 = ('01' * i)[:i]
            board0 += gen0
            board1 += gen1
        print(len(board0), wild_towers(board0), wild_towers(board1))

def test_can_solve_full_squares():
    for i in range(1, 10):
        assert wild_towers('1' * (i * i)) == math.factorial(i)

