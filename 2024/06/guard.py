import os
from enum import Enum

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

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
        return result


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def in_bounds_pos(grid, pos):
    return in_bounds(grid, pos[0], pos[1])


def add_direction(pos, direction: Direction):
    return (pos[0] + direction.value[0], pos[1] + direction.value[1])


def task1():
    guard_pos, grid = load_input()
    guard_direction = Direction.UP
    while in_bounds_pos(grid, guard_pos):
        grid[guard_pos[0]][guard_pos[1]] = "X"
        guard_pos_new = add_direction(guard_pos, guard_direction)
        if not in_bounds_pos(grid, guard_pos_new):
            break

        if grid[guard_pos_new[0]][guard_pos_new[1]] == "#":
            guard_direction = guard_direction.turn_90_right()
        else:
            guard_pos = guard_pos_new
    return sum(row.count("X") for row in grid)


def task2():
    guard_pos_start, grid = load_input()
    result = 0
    possible_obstructions = set()
    guard_pos = guard_pos_start
    guard_direction = Direction.UP
    while in_bounds_pos(grid, guard_pos):
        if guard_pos != guard_pos_start:
            possible_obstructions.add(guard_pos)
        guard_pos_new = add_direction(guard_pos, guard_direction)
        if not in_bounds_pos(grid, guard_pos_new):
            break

        if grid[guard_pos_new[0]][guard_pos_new[1]] == "#":
            guard_direction = guard_direction.turn_90_right()
        else:
            guard_pos = guard_pos_new

    for obstruction in possible_obstructions:
        visited = set()
        guard_pos = guard_pos_start
        guard_direction = Direction.UP
        while in_bounds_pos(grid, guard_pos):
            if (guard_pos, guard_direction) in visited:
                result += 1
                break
            visited.add((guard_pos, guard_direction))
            guard_pos_new = add_direction(guard_pos, guard_direction)
            if not in_bounds_pos(grid, guard_pos_new):
                break

            if grid[guard_pos_new[0]][guard_pos_new[1]] == "#" or guard_pos_new == obstruction:
                guard_direction = guard_direction.turn_90_right()
            else:
                guard_pos = guard_pos_new
    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        for i, line in enumerate(grid):
            try:
                index = line.index("^")
                line[index] = "."
                return (i, index), grid
            except ValueError:
                pass
        raise RuntimeError


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
