import os
import re
import time
from datetime import timedelta

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def calculate_checksum(filesystem):
    checksum = 0
    for i, block_id in enumerate(filesystem):
        if block_id is not None:
            checksum += i * block_id
    return checksum


def task1():
    pairs = load_input()
    filesystem = []
    empty_count = 0
    for i, (filled, empty) in enumerate(pairs):
        filesystem += [i] * filled + [None] * empty
        empty_count += empty

    # Fixes an edgecase crash
    filesystem += [None]

    for _ in range(empty_count):
        index = filesystem.index(None)
        filesystem[index] = filesystem.pop()
    return calculate_checksum(filesystem)


def task2():
    pairs = load_input()
    pairs = list(zip(range(len(pairs)), pairs))
    indices = {x: x for x in range(len(pairs))}
    for i in reversed(range(len(pairs))):
        index = indices[i]
        pair = pairs[index]
        for j in range(index):
            pair2 = pairs[j]
            if pair2[1][1] >= pair[1][0]:
                free_after = pair2[1][1]
                pairs[j] = (pair2[0], (pair2[1][0], 0))
                pre_index = index - 1
                pre_free = pairs[pre_index][1][1] + (sum(pair[1]) if pre_index != j else 0)
                pairs[pre_index] = (pairs[pre_index][0], (pairs[pre_index][1][0], pre_free))
                pairs.pop(index)
                free_after = (
                    (free_after - pair[1][0]) if pre_index != j else (free_after + pair[1][1])
                )
                pairs.insert(j + 1, (pair[0], (pair[1][0], free_after)))
                for k in indices:
                    if indices[k] == index:
                        indices[k] = j + 1
                    elif j < indices[k] < index:
                        indices[k] += 1
                break

    filesystem = []
    for i, (filled, empty) in pairs:
        filesystem += [i] * filled + [None] * empty

    return calculate_checksum(filesystem)


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        text = inp.read().strip() + "0"
        pairs = tuple(map(lambda x: (int(x[0]), int(x[1])), re.findall(r"(\d)(\d)", text)))
        return pairs


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
