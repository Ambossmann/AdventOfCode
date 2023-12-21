import os
import re
import numpy as np

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)

DIRECTIONS = (RIGHT, DOWN, LEFT, UP)

def task1():
    garden, start = load_input()
    return calculate_reachable(64, garden, start)

def task2():
    garden, start = load_input()
    for i in range(len(garden)):
        garden[i] = garden[i] * 5
    garden = garden * 5
    start = (start[0] + 131*2, start[1] + 131*2)
    value0 = calculate_reachable(65, garden, start)
    value1 = calculate_reachable(65+131, garden, start)
    value2 = calculate_reachable(65+131*2, garden, start)
    extrapolator = np.poly1d(np.polyfit((0, 1, 2), (value0, value1, value2), 2))
    return round(extrapolator(202_300))

def calculate_reachable(steps, garden, start):
    calculated = set()
    number_of_steps = [set() for i in range(steps + 1)]

    number_of_steps[0].add(start)
    calculated.add(start)

    for i in range(steps):
        for tile in number_of_steps[i]:
            for d in DIRECTIONS:
                    new_tile = (tile[0] + d[0], tile[1] + d[1])
                    if valid_coords(new_tile, garden) and (not new_tile in calculated) and garden[new_tile[0]][new_tile[1]] != "#":
                        number_of_steps[i+1].add(new_tile)
                        calculated.add(new_tile)
    if steps % 2 == 0:
        return sum(len(l) for l in number_of_steps[::2])
    else:
        return sum(len(l) for l in number_of_steps[1::2])



def valid_coords(coords, grid):
    return 0 <= coords[0] < len(grid) and 0 <= coords[1] < len(grid[0]) 

def load_input():
    with open(input_file) as input:
        text = [[c for c in line] for line in input.read().splitlines()]
        for i in range(len(text)):
            for j in range(len(text[0])):
                if text[i][j] == "S":
                    start = (i, j)
                    break

    return text, start

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()