import os
import re
import time
from datetime import timedelta

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

width = 101
height = 103


def task1():
    robots = load_input()
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    nums_steps = 100
    for robot in robots:
        end_pos = (
            (robot[0] + robot[2] * nums_steps) % width,
            (robot[1] + robot[3] * nums_steps) % height,
        )
        if end_pos[0] < width >> 1:
            if end_pos[1] < height >> 1:
                q1 += 1
            elif end_pos[1] > height >> 1:
                q3 += 1
        elif end_pos[0] > width >> 1:
            if end_pos[1] < height >> 1:
                q2 += 1
            elif end_pos[1] > height >> 1:
                q4 += 1

    return q1 * q2 * q3 * q4


def task2():
    robots = load_input()
    nums_steps = 0
    while True:
        positions = set()
        for robot in robots:
            end_pos = (
                (robot[0] + robot[2] * nums_steps) % width,
                (robot[1] + robot[3] * nums_steps) % height,
            )
            positions.add(end_pos)
        if len(positions) == len(robots):
            break
        nums_steps += 1

    return nums_steps


def print_tree(nums_steps):
    robots = load_input()
    grid = [[0 for i in range(width)] for j in range(height)]
    for robot in robots:
        end_x = (robot[0] + robot[2] * nums_steps) % width
        end_y = (robot[1] + robot[3] * nums_steps) % height
        grid[end_y][end_x] += 1

    print("\n".join("".join(map(str, line)) for line in grid))


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return tuple(
            map(
                lambda x: list(map(int, x)),
                re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", inp.read()),
            )
        )


def main():
    start = time.perf_counter()
    task1_output = task1()
    end = time.perf_counter()
    print(f"Task 1: Result: {task1_output} Execution time: {timedelta(seconds=end-start)}")

    start = time.perf_counter()
    task2_output = task2()
    end = time.perf_counter()
    print(f"Task 2: Result: {task2_output} Execution time: {timedelta(seconds=end-start)}")

    # print_tree(task2_output)


if __name__ == "__main__":
    main()
