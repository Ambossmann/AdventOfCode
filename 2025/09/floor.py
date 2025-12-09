import os
import re
import time
from datetime import timedelta
from functools import reduce
from itertools import chain, combinations, islice, pairwise
from math import sqrt
from operator import itemgetter, mul

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def distance(a, b):
    return sqrt(sum(map(lambda x: (x[0] - x[1]) ** 2, zip(a, b))))


def border_touches_rect(rect, border):
    assert border[0][0] == border[1][0] or border[0][1] == border[1][1]
    if border[0][0] == border[1][0]:
        b_x = border[0][0]
        if b_x < rect[0][0] or b_x > rect[1][0]:
            return False
        b_min_y = min(border[0][1], border[1][1])
        b_max_y = max(border[0][1], border[1][1])
        return b_min_y <= rect[1][1] and b_max_y >= rect[0][1]
    else:
        b_y = border[0][1]
        if b_y < rect[0][1] or b_y > rect[1][1]:
            return False
        b_min_x = min(border[0][0], border[1][0])
        b_max_x = max(border[0][0], border[1][0])
        return b_min_x <= rect[1][0] and b_max_x >= rect[0][0]


def border_goes_through_rect(rect, border):
    if border[0][0] == border[1][0]:
        b_x = border[0][0]
        b_min_y = min(border[0][1], border[1][1])
        b_max_y = max(border[0][1], border[1][1])
        return (rect[0][0] < b_x < rect[1][0]) and (b_min_y < rect[1][1] and b_max_y > rect[0][1])
    else:
        b_y = border[0][1]
        b_min_x = min(border[0][0], border[1][0])
        b_max_x = max(border[0][0], border[1][0])
        return (rect[0][1] < b_y < rect[1][1]) and (b_min_x < rect[1][0] and b_max_x > rect[0][0])


def border_kills_rect(rect, border):
    if not border_touches_rect(rect, border):
        return False

    if border_goes_through_rect(rect, border):
        return True

    # It shouldn't work yet, but it does.
    return False


def task1():
    reds, _ = load_input()

    max_size = 0

    for a, b in combinations(reds, 2):
        min_x = min(a[0], b[0])
        max_x = max(a[0], b[0])
        min_y = min(a[1], b[1])
        max_y = max(a[1], b[1])
        size = (max_x - min_x + 1) * (max_y - min_y + 1)
        if size > max_size:
            max_size = size

    return max_size


def task2():
    reds, borders = load_input()

    max_size = 0

    for a, b in combinations(reds, 2):
        min_x = min(a[0], b[0])
        max_x = max(a[0], b[0])
        min_y = min(a[1], b[1])
        max_y = max(a[1], b[1])
        size = (max_x - min_x + 1) * (max_y - min_y + 1)
        if size > max_size:
            for bo in borders:
                if border_kills_rect(((min_x, min_y), (max_x, max_y)), bo):
                    break
            else:
                max_size = size

    # print(borders)
    return max_size


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        reds = list(
            map(
                lambda x: (int(x[0]), int(x[1])),
                re.findall(r"(\d+),(\d+)", inp.read()),
            )
        )

        borders = list(pairwise(chain(reds, islice(reds, 1))))

        return reds, borders


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
