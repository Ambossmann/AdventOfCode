import os
import re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    ranges, ids = load_input()
    fresh = 0
    for i in ids:
        for lower, upper in ranges:
            if lower <= i <= upper:
                fresh += 1
                break
    return fresh


def task2():
    ranges, _ = load_input()
    for i, (lower, upper) in enumerate(ranges):
        while True:
            for j in range(i + 1, len(ranges)):
                lower2, upper2 = ranges[j]
                if (
                    lower <= lower2 <= upper
                    or lower <= upper2 <= upper
                    or lower2 <= lower <= upper2
                    or lower2 <= upper <= upper2
                ):
                    lower = min(lower, lower2)
                    upper = max(upper, upper2)
                    ranges[i] = (lower, upper)
                    ranges.pop(j)
                    break
            else:
                break

    fresh = 0
    for lower, upper in ranges:
        fresh += upper - lower + 1

    return fresh


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        ranges, ids = inp.read().split("\n\n")
        ranges = list(
            map(
                lambda x: (int(x[0]), int(x[1])),
                re.findall(r"(\d+)-(\d+)", ranges),
            )
        )
        ids = list(
            map(
                int,
                re.findall(r"(\d+)", ids),
            )
        )
        return ranges, ids


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
