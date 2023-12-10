import re
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    with open(input_file) as input:
        text = input.read()
        left_right_instructions = tuple(0 if rl == "L" else 1 for rl in text.splitlines()[0].rstrip())
        instructions = re.findall(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", text)
        instructions = {i[0]: i[1:] for i in instructions}
        next_instruction = "AAA"
        instruction_count = 0
        left_right_index = 0
        while next_instruction != "ZZZ":
            next_instruction = instructions[next_instruction][left_right_instructions[left_right_index]]
            instruction_count += 1
            left_right_index = (left_right_index + 1) % len(left_right_instructions)
        return instruction_count    

def task2():
    result = 0
    with open(input_file) as input:
        text = input.read()
        left_right_instructions = tuple(0 if rl == "L" else 1 for rl in text.splitlines()[0].rstrip())
        instructions = re.findall(r"([A-Z\d]{3}) = \(([A-Z\d]{3}), ([A-Z\d]{3})\)", text)
        instructions = {i[0]: i[1:] for i in instructions}
        start_instructions = re.findall(r"([A-Z\d]{2}A) = \([A-Z\d]{3}, [A-Z\d]{3}\)", text)
        cirle_lengths = tuple(get_circle_length(start_instruction, instructions, left_right_instructions) for start_instruction in start_instructions)
        return math.lcm(*cirle_lengths)

def get_circle_length(start_instruction, instructions, left_right_instructions):
    left_right_index = 0
    next_instruction = start_instruction
    while next_instruction[2] != "Z":
        next_instruction = instructions[next_instruction][left_right_instructions[left_right_index]]
        left_right_index = (left_right_index + 1) % len(left_right_instructions)
    cycle_start = next_instruction
    instruction_count = 0
    while next_instruction != cycle_start or instruction_count == 0:
        next_instruction = instructions[next_instruction][left_right_instructions[left_right_index]]
        instruction_count += 1
        left_right_index = (left_right_index + 1) % len(left_right_instructions)
    return instruction_count

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()