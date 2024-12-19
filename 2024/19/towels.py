import os
import time
from datetime import timedelta
from functools import cache

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


@cache
def match_design_rec(towels: list[str], design_remnant: str):
    if len(design_remnant) == 0:
        return True
    for towel in towels:
        if design_remnant.startswith(towel):
            if match_design_rec(towels, design_remnant[len(towel) :]):
                return True
    return False


def task1():
    towels, designs = load_input()
    result = 0
    for design in designs:
        if match_design_rec(towels, design):
            result += 1

    return result


@cache
def count_arrangements_rec(towels: list[str], design_remnant: str):
    if len(design_remnant) == 0:
        return 1
    result = 0
    for towel in towels:
        if design_remnant.startswith(towel):
            result += count_arrangements_rec(towels, design_remnant[len(towel) :])
    return result


def task2():
    towels, designs = load_input()
    result = 0
    for design in designs:
        result += count_arrangements_rec(towels, design)

    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:

        towel_text, design_text = inp.read().split("\n\n")

        towels = tuple(towel_text.split(", "))

        designs = design_text.splitlines()

        return towels, designs


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
