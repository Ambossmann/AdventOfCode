import os
import time
from collections import Counter
from datetime import timedelta
from functools import cache

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

button_pos_on_keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

button_pos_on_directional_control = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


@cache
def move(pos, button_pos, invalid_pos):
    distance_i = button_pos[0] - pos[0]
    distance_j = button_pos[1] - pos[1]

    sequence = []

    if distance_i == 0:
        sequence.append(distance_j * ">" if distance_j > 0 else -distance_j * "<")

    elif distance_j == 0:
        sequence.append(distance_i * "v" if distance_i > 0 else -distance_i * "^")

    elif distance_j < 0 and (pos[0], button_pos[1]) != invalid_pos:
        sequence.append(distance_j * ">" if distance_j > 0 else -distance_j * "<")
        sequence.append(distance_i * "v" if distance_i > 0 else -distance_i * "^")

    elif (button_pos[0], pos[1]) != invalid_pos:
        sequence.append(distance_i * "v" if distance_i > 0 else -distance_i * "^")
        sequence.append(distance_j * ">" if distance_j > 0 else -distance_j * "<")

    elif (pos[0], button_pos[1]) != invalid_pos:
        sequence.append(distance_j * ">" if distance_j > 0 else -distance_j * "<")
        sequence.append(distance_i * "v" if distance_i > 0 else -distance_i * "^")

    sequence.append("A")

    return "".join(sequence)


@cache
def find_sequence(desired_sequence, is_keypad):
    invalid_pos, button_pos_dict = (
        ((3, 0), button_pos_on_keypad) if is_keypad else ((0, 0), button_pos_on_directional_control)
    )
    pos = button_pos_dict["A"]
    sequence = []
    for button in desired_sequence:
        button_pos = button_pos_dict[button]
        sequence.append(move(pos, button_pos, invalid_pos))

        pos = button_pos
    return sequence


def count_sequences(sequences: Counter, is_keypad) -> Counter:
    result = Counter()
    for sequence in sequences:
        count = Counter(find_sequence(sequence, is_keypad))
        for k in count.keys():
            count[k] *= sequences[sequence]
        result.update(count)
    return result


def calculate_complexity(indirections):
    instructions = load_input()
    result = 0
    for instruction in instructions:
        count = Counter()
        count[instruction] = 1
        count = count_sequences(count, True)
        for _ in range(indirections):
            count = count_sequences(count, False)
        sequence_length = sum(c * len(s) for s, c in count.items())
        result += int(instruction[:-1]) * sequence_length

    return result


def task1():
    return calculate_complexity(2)


def task2():
    return calculate_complexity(25)


def load_input():
    with open(input_file, encoding="utf-8") as inp:

        instructions = inp.read().splitlines()

        return instructions


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
