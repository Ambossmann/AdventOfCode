import os
import re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    ranges = load_input()
    invalid_sum = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            si = str(i)
            middle = len(si) // 2
            if si[:middle] == si[middle:]:
                invalid_sum += i
    return invalid_sum


def task2():
    ranges = load_input()
    invalid_sum = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            si = str(i)
            for j in range(1, (len(si) // 2) + 1):
                if len(si) % j == 0:
                    if si == si[:j] * (len(si) // j):
                        invalid_sum += i
                        break
    return invalid_sum


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return list(
            map(
                lambda x: (int(x[0]), int(x[1])),
                re.findall(r"(\d*)-(\d*)", inp.read()),
            )
        )


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
