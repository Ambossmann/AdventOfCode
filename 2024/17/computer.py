import os
import time
from datetime import timedelta

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def get_combo_value(operand, a, b, c):
    match operand:
        case 0 | 1 | 2 | 3:
            value = operand
        case 4:
            value = a
        case 5:
            value = b
        case 6:
            value = c
        case _:
            raise ValueError
    return value


def compute(instructions, a, b, c):
    pc = 0
    output = []
    while pc < len(instructions) - 1:
        instruction = instructions[pc]
        operand = instructions[pc + 1]
        match instruction:
            case 0:
                a = int(a / (2 ** get_combo_value(operand, a, b, c)))
            case 1:
                b = b ^ operand
            case 2:
                b = get_combo_value(operand, a, b, c) % 8
            case 3:
                if a != 0:
                    pc = operand
                    continue
            case 4:
                b = b ^ c
            case 5:
                output.append(get_combo_value(operand, a, b, c) % 8)
            case 6:
                b = int(a / (2 ** get_combo_value(operand, a, b, c)))
            case 7:
                c = int(a / (2 ** get_combo_value(operand, a, b, c)))
        pc += 2
    return output


def task1():
    a, b, c, instructions = load_input()
    output = compute(instructions, a, b, c)

    return ",".join(map(str, output))


def check_recursive(a_test, b, c, instructions, i):
    if i < 0:
        return None
    for j in range(0, 8):
        a = a_test | (j << i * 3)
        output = compute(instructions, a, b, c)

        if i == 0 and tuple(output) == instructions:
            return a

        if len(output) == len(instructions) and output[i] == instructions[i]:
            possible_solution = check_recursive(a, b, c, instructions, i - 1)
            if possible_solution:
                return possible_solution

    return None


def task2():
    a, b, c, instructions = load_input()

    a = check_recursive(0, b, c, instructions, len(instructions) - 1)

    return a


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        a = int(inp.readline().split()[2].strip())
        b = int(inp.readline().split()[2].strip())
        c = int(inp.readline().split()[2].strip())
        inp.readline()
        instructions = tuple(map(int, inp.readline().split()[1].strip().split(",")))
        return a, b, c, instructions


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
