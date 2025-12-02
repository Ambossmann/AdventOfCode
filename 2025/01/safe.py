import os
import re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    rotations = load_input()
    current = 50
    zeroes = 0
    for rotation in rotations:
        current = (current + rotation) % 100
        if current == 0:
            zeroes += 1
    return zeroes


def task2():
    rotations = load_input()
    current = 50
    zeroes = 0
    for rotation in rotations:
        for _ in range(abs(rotation)):
            current = (current + (1 if rotation >= 0 else -1)) % 100
            if current == 0:
                zeroes += 1
    return zeroes


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return list(
            map(
                lambda x: int(x[1]) * (-1 if x[0] == "L" else 1),
                re.findall(r"(L|R)(\d*)", inp.read()),
            )
        )


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
