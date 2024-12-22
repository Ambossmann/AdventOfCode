import os
import time
from collections import Counter
from datetime import timedelta

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

PRUNE_MASK = 2**24 - 1


def next_number(number):
    number ^= number << 6
    number &= PRUNE_MASK
    number ^= number >> 5
    number &= PRUNE_MASK
    number ^= number << 11
    number &= PRUNE_MASK
    return number


def task1():
    numbers = load_input()
    result = 0
    for number in numbers:
        for _ in range(2000):
            number = next_number(number)
        result += number
    return result


def task2():
    numbers = load_input()
    count = Counter()
    for number in numbers:
        prev = number % 10
        sequence = (None, None, None, None)
        used_seqences = set()
        for _ in range(2000):
            number = next_number(number)
            price = number % 10
            sequence = sequence[1:] + (price - prev,)
            prev = price
            if sequence[0] is not None and sequence not in used_seqences:
                count[sequence] += price
                used_seqences.add(sequence)
    return count.most_common(1)[0][1]


def load_input():
    with open(input_file, encoding="utf-8") as inp:

        numbers = list(map(int, inp.read().splitlines()))

        return numbers


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
