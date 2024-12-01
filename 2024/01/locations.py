import os
import re
from collections import Counter

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    ids1, ids2 = zip(*load_input())
    combined = tuple(zip(sorted(ids1), sorted(ids2)))
    difference = tuple(map(lambda x: abs(x[0] - x[1]), combined))
    return sum(difference)


def task2():
    ids1, ids2 = zip(*load_input())
    counts = Counter(ids1)
    return sum(map(lambda x: x * counts[x], ids2))


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return list(
            map(
                lambda x: (int(x[0]), int(x[1])),
                re.findall(r"(\d*)   (\d*)", inp.read()),
            )
        )


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
