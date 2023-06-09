import pathlib
import typing as tp
from copy import deepcopy
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i * n:(i + 1) * n] for i in range(n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    # print(pos)
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [grid[i][pos[1]] for i in range(len(grid[0]))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    a, b = (pos[0]) // 3, (pos[1]) // 3
    return [grid[i][j] for i in range(a * 3, (a + 1) * 3) for j in range(b * 3, (b + 1) * 3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    n = len(grid[0])
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '.':
                return ((i, j))
    return -1


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    # if pos == -1:
    #    return []
    maybe = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for i in get_row(grid, pos):
        if i in maybe:
            maybe.remove(i)
    for i in get_col(grid, pos):
        if i in maybe:
            maybe.remove(i)
    for i in get_block(grid, pos):
        if i in maybe:
            maybe.remove(i)
    return maybe


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    
    Траблы с подстановкой нужных цифр
    
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    position = find_empty_positions(grid)
    if position == -1:
        #display(grid)
        return grid
    values = find_possible_values(grid, position)
    if not values:
        return 0
    checkpoint = []
    for i in values:
        checkpoint.append(deepcopy(grid))
        grid[position[0]][position[1]] = i
        grid = solve(grid)
        if not grid:
            grid = deepcopy(checkpoint.pop())
            continue
        else:
            return grid

def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    clist = set()
    rlist = set()
    blist = set()
    #print(solution)
    n = len(solution[0])
    for i in range(n):
        for j in get_col(solution, (0, i)):
            if j not in clist:
                clist.add(j)
        if len(clist) != 9:
            return False
        for j in get_row(solution, (i, 0)):
            if j not in rlist:
                rlist.add(j)
        if len(rlist) != 9:
            return False
    for i in range(0, n, 3):
        for j in range(0, n, 3):
            for k in get_block(solution, (i, j)):
                if k not in blist:
                    blist.add(k)
            if len(blist) != 9:
                return False
    if '.' in clist or '.' in rlist or '.' in blist:
        return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    sudoku = [['.'] * 9 for i in range(9)]
    i = 0
    while i < 9:
        j = random.randint(0, 8)
        impossible = get_block(sudoku, (i, i))
        n = str(random.randint(1, 9))
        dots = impossible.count('.')
        for K in range(dots):
            impossible.remove('.')

        if n not in impossible:
            sudoku[i][i] = n
            i += 1

    sudoku = solve(sudoku)
    M = 81 - N
    while M > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if sudoku[i][j] == '.':
            continue
        else:
            sudoku[i][j] = '.'
            M -= 1
    return sudoku
    '''
   for i in range(0, 9, 3):
        possible = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        while possible:
            n = possible[-1]
            j = random.randint(0, 8)
            impossible = get_col(sudoku, (i, j)) + get_row(sudoku, (i,j))
            dots = impossible.count('.')
            for K in range(dots):
                impossible.remove('.')
            if sudoku[i][j] == '.' and n not in impossible:
                display(sudoku)
                sudoku[i][j] = possible.pop()
            else:
                print(n, impossible)
                display(sudoku)
        '''




if __name__ == "__main__":
    for fname in ["custom.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
