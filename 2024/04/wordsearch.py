import os
from enum import Enum

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)

    def reverse(self):
        match self:
            case self.UP:
                result = self.DOWN
            case self.DOWN:
                result = self.UP
            case self.LEFT:
                result = self.RIGHT
            case self.RIGHT:
                result = self.LEFT
            case self.UP_LEFT:
                result = self.DOWN_RIGHT
            case self.UP_RIGHT:
                result = self.DOWN_LEFT
            case self.DOWN_LEFT:
                result = self.UP_RIGHT
            case self.DOWN_RIGHT:
                result = self.UP_LEFT
        return result

    def turn_90_right(self):
        match self:
            case self.UP:
                result = self.RIGHT
            case self.DOWN:
                result = self.LEFT
            case self.LEFT:
                result = self.UP
            case self.RIGHT:
                result = self.DOWN
            case self.UP_LEFT:
                result = self.UP_RIGHT
            case self.UP_RIGHT:
                result = self.DOWN_RIGHT
            case self.DOWN_LEFT:
                result = self.UP_LEFT
            case self.DOWN_RIGHT:
                result = self.DOWN_LEFT
        return result

    def is_diagonal(self):
        return self in (self.UP_LEFT, self.UP_RIGHT, self.DOWN_LEFT, self.DOWN_RIGHT)


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def search_xmas(grid, row, col):
    result = 0
    for direction in Direction:
        mas = list("MAS")
        new_row = row
        new_col = col
        while mas:
            c = mas.pop(0)
            offset_row, offset_col = direction.value
            new_row += offset_row
            new_col += offset_col
            if in_bounds(grid, new_row, new_col):
                if grid[new_row][new_col] != c:
                    break
            else:
                break
        else:
            result += 1
    return result


def search_x_shaped_mas(grid, row, col):
    for direction in Direction:
        if direction.is_diagonal():
            offset_row, offset_col = direction.value
            offset_row_r, offset_col_r = direction.reverse().value
            new_row = row + offset_row
            new_col = col + offset_col
            new_row_r = row + offset_row_r
            new_col_r = col + offset_col_r
            if in_bounds(grid, new_row, new_col) and in_bounds(grid, new_row_r, new_col_r):
                if grid[new_row][new_col] == "M" and grid[new_row_r][new_col_r] == "S":
                    direction_t = direction.turn_90_right()
                    offset_row_t, offset_col_t = direction_t.value
                    offset_row_tr, offset_col_tr = direction_t.reverse().value
                    new_row_t = row + offset_row_t
                    new_col_t = col + offset_col_t
                    new_row_tr = row + offset_row_tr
                    new_col_tr = col + offset_col_tr
                    if in_bounds(grid, new_row_t, new_col_t) and in_bounds(
                        grid, new_row_tr, new_col_tr
                    ):
                        if (
                            grid[new_row_t][new_col_t] == "M"
                            and grid[new_row_tr][new_col_tr] == "S"
                        ):
                            return 1
    return 0


def task1():
    grid = load_input()
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                result += search_xmas(grid, i, j)
    return result


def task2():
    grid = load_input()
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "A":
                result += search_x_shaped_mas(grid, i, j)
    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return tuple(map(lambda x: list(x.strip()), inp.readlines()))


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
