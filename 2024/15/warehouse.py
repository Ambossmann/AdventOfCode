import os
import time
from datetime import timedelta
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

    def add_to_pos(self, pos):
        return (pos[0] + self.value[0], pos[1] + self.value[1])


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def in_bounds_pos(grid, pos):
    return in_bounds(grid, pos[0], pos[1])


def set_in_range(row_start, row_end, col_start, col_end, grid, value):
    if row_start > row_end:
        row_start, row_end = row_end, row_start
    if col_start > col_end:
        col_start, col_end = col_end, col_start
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            grid[i][j] = value


def task1():
    grid, directions, robot_pos = load_input()
    for d in directions:
        target_pos = d.add_to_pos(robot_pos)
        pos = target_pos
        while True:
            match grid[pos[0]][pos[1]]:
                case "O":
                    pass
                case "#":
                    break
                case ".":
                    set_in_range(pos[0], target_pos[0], pos[1], target_pos[1], grid, "O")
                    grid[target_pos[0]][target_pos[1]] = "@"
                    grid[robot_pos[0]][robot_pos[1]] = "."
                    robot_pos = target_pos
                    break
            pos = d.add_to_pos(pos)

    result = 0
    for i, line in enumerate(grid):
        for j, v in enumerate(line):
            if v == "O":
                result += 100 * i + j
    return result


def widen_tile(tile):
    match tile:
        case "O":
            return ["[", "]"]
        case "#":
            return ["#", "#"]
        case ".":
            return [".", "."]
        case "@":
            return ["@", "."]
        case _:
            raise ValueError


def task2():
    grid, directions, robot_pos = load_input()
    for i, line in enumerate(grid):
        grid[i] = []
        for p in map(widen_tile, line):
            grid[i].extend(p)
    robot_pos = (robot_pos[0], robot_pos[1] * 2)

    for d in directions:
        target_pos = d.add_to_pos(robot_pos)
        pos = target_pos
        crates = []
        new_positions = [pos]
        while new_positions:
            pos = new_positions.pop(0)
            match grid[pos[0]][pos[1]]:
                case "[":
                    crates.append(pos)
                    if d != Direction.RIGHT:
                        new_positions.append(d.add_to_pos(pos))
                    if d != Direction.LEFT:
                        new_positions.append(d.add_to_pos((pos[0], pos[1] + 1)))
                case "]":
                    crates.append((pos[0], pos[1] - 1))
                    if d != Direction.LEFT:
                        new_positions.append(d.add_to_pos(pos))
                    if d != Direction.RIGHT:
                        new_positions.append(d.add_to_pos((pos[0], pos[1] - 1)))
                case "#":
                    break
                case ".":
                    pass
        else:
            for crate in crates:
                grid[crate[0]][crate[1]] = "."
                grid[crate[0]][crate[1] + 1] = "."

            for crate in crates:
                moved = d.add_to_pos(crate)
                grid[moved[0]][moved[1]] = "["
                grid[moved[0]][moved[1] + 1] = "]"

            grid[target_pos[0]][target_pos[1]] = "@"
            grid[robot_pos[0]][robot_pos[1]] = "."
            robot_pos = target_pos

    result = 0
    for i, line in enumerate(grid):
        for j, v in enumerate(line):
            if v == "[":
                result += 100 * i + j
    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid_text, directions_text = inp.read().split("\n\n")
        grid = list(map(lambda x: list(x.strip()), grid_text.splitlines()))
        for i, line in enumerate(grid):
            try:
                robot_pos = (i, line.index("@"))
                break
            except ValueError:
                pass

        directions_text = directions_text.replace("\n", "")
        directions = []
        for d in directions_text:
            match d:
                case "^":
                    directions.append(Direction.UP)
                case "v":
                    directions.append(Direction.DOWN)
                case "<":
                    directions.append(Direction.LEFT)
                case ">":
                    directions.append(Direction.RIGHT)

        return grid, directions, robot_pos


def main():
    start = time.perf_counter()
    task1_output = task1()
    end = time.perf_counter()
    print(f"Task 1: Result: {task1_output} Execution time: {timedelta(seconds=end-start)}")

    start = time.perf_counter()
    task2_output = task2()
    end = time.perf_counter()
    print(f"Task 2: Result: {task2_output} Execution time: {timedelta(seconds=end-start)}")


if __name__ == "__main__":
    main()
