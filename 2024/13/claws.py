import os
import re
import time
from datetime import timedelta

from sympy import solve
from sympy.abc import a, b
from sympy.utilities.misc import as_int

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    claw_machines = load_input()
    result = 0
    for claw_machine in claw_machines:
        a_x, a_y, b_x, b_y, p_x, p_y = claw_machine
        equations = [a * a_x + b * b_x - p_x, a * a_y + b * b_y - p_y]
        solutions = solve(equations, a, b, set=True)
        try:
            solution: dict = solutions[1].pop()
            a_v = as_int(solution[0], strict=True)
            b_v = as_int(solution[1], strict=True)
            result += 3 * a_v + b_v
        except ValueError:
            pass

    return result


def task2():
    claw_machines = load_input()
    result = 0
    for claw_machine in claw_machines:
        a_x, a_y, b_x, b_y, p_x, p_y = claw_machine
        equations = [
            a * a_x + b * b_x - p_x - 10000000000000,
            a * a_y + b * b_y - p_y - 10000000000000,
        ]
        solutions = solve(equations, a, b, set=True)
        try:
            solution: dict = solutions[1].pop()
            a_v = as_int(solution[0], strict=True)
            b_v = as_int(solution[1], strict=True)
            result += 3 * a_v + b_v
        except ValueError:
            pass

    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return tuple(
            map(
                lambda x: tuple(map(int, x)),
                re.findall(
                    r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
                    inp.read(),
                ),
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


if __name__ == "__main__":
    main()
