import os
import time
from datetime import timedelta
from functools import cache

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


@cache
def stone_count_after_steps(num: int, steps: int):
    if steps == 0:
        return 1
    if num == 0:
        return stone_count_after_steps(1, steps - 1)
    s = str(num)
    s_len = len(s)
    if s_len % 2 == 0:
        return stone_count_after_steps(int(s[: s_len >> 1]), steps - 1) + stone_count_after_steps(
            int(s[s_len >> 1 :]), steps - 1
        )
    return stone_count_after_steps(num * 2024, steps - 1)


def task1():
    nums = load_input()
    return sum(map(lambda x: stone_count_after_steps(x, 25), nums))


def task2():
    nums = load_input()
    return sum(map(lambda x: stone_count_after_steps(x, 75), nums))


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return list(map(int, inp.read().strip().split()))


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
