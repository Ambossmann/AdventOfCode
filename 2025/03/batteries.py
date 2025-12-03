import os
import re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def max_joltage(bank, battery_count):
    maxs = [0 for _ in range(battery_count)]
    for i, battery in enumerate(bank):
        for j, m in enumerate(maxs):
            if battery > m and i < len(bank) - (battery_count - j - 1):
                maxs[j] = battery
                for k in range(j + 1, battery_count):
                    maxs[k] = 0
                break
    joltage = 0
    for m in maxs:
        joltage *= 10
        joltage += m
    return joltage


def task1():
    banks = load_input()
    joltage = 0
    for bank in banks:
        joltage += max_joltage(bank, 2)
    return joltage


def task2():
    banks = load_input()
    joltage = 0
    for bank in banks:
        joltage += max_joltage(bank, 12)
    return joltage


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return list(
            map(
                lambda x: [int(d) for d in x],
                re.findall(r"(\d*)\n", inp.read()),
            )
        )


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
