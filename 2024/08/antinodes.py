import itertools
import os
import string

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def in_bounds_pos(grid, pos):
    return in_bounds(grid, pos[0], pos[1])


def task1():
    grid, antennas_by_freqency = load_input()
    antinode_positions = set()
    for antenna_positions in antennas_by_freqency.values():
        antenna_combinations = itertools.combinations(antenna_positions, 2)
        for (a1y, a1x), (a2y, a2x) in antenna_combinations:
            diff_x = a2x - a1x
            diff_y = a2y - a1y
            pos1 = (a1y - diff_y, a1x - diff_x)
            pos2 = (a2y + diff_y, a2x + diff_x)
            if in_bounds_pos(grid, pos1):
                antinode_positions.add(pos1)
            if in_bounds_pos(grid, pos2):
                antinode_positions.add(pos2)
    return len(antinode_positions)


def task2():
    grid, antennas_by_freqency = load_input()
    antinode_positions = set()
    for antenna_positions in antennas_by_freqency.values():
        antenna_combinations = itertools.combinations(antenna_positions, 2)
        for (a1x, a1y), (a2x, a2y) in antenna_combinations:
            diff_x = a2x - a1x
            diff_y = a2y - a1y
            p1y = a1y
            p1x = a1x
            p2y = a2y
            p2x = a2x

            while in_bounds(grid, p1x, p1y) or in_bounds(grid, p2x, p2y):
                pos1 = (p1x, p1y)
                pos2 = (p2x, p2y)
                if in_bounds_pos(grid, pos1):
                    antinode_positions.add(pos1)
                if in_bounds_pos(grid, pos2):
                    antinode_positions.add(pos2)

                p1y -= diff_y
                p1x -= diff_x
                p2y += diff_y
                p2x += diff_x
    return len(antinode_positions)


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        valid_freqencys = set(string.ascii_letters + string.digits)
        antennas_by_freqency = {}
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c in valid_freqencys:
                    if not c in antennas_by_freqency:
                        antennas_by_freqency[c] = []
                    antennas_by_freqency[c].append((i, j))
        return grid, antennas_by_freqency


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
