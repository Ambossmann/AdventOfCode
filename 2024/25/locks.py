import os
import time
from datetime import timedelta

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    locks, keys = load_input()

    result = 0

    for lock in locks:
        for key in keys:
            if all(lock[i] + key[i] <= 5 for i in range(5)):
                result += 1

    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        texts = inp.read().split("\n\n")

        locks = set()
        keys = set()

        for text in texts:
            t = text[0]
            h = [-1] * 5
            for line in text.splitlines():
                h[0] += 1 if line[0] == "#" else 0
                h[1] += 1 if line[1] == "#" else 0
                h[2] += 1 if line[2] == "#" else 0
                h[3] += 1 if line[3] == "#" else 0
                h[4] += 1 if line[4] == "#" else 0
            h = tuple(h)
            if t == "#":
                locks.add(h)
            else:
                keys.add(h)

        return locks, keys


def main():
    start = time.perf_counter()
    task1_output = task1()
    end = time.perf_counter()
    print(f"Task 1: Result: {task1_output} Execution time: {timedelta(seconds=end-start)}")


if __name__ == "__main__":
    main()
