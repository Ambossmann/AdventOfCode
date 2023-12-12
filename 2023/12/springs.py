import re
import os
import itertools
from functools import cache

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

# unknown_pattern = re.compile(r"\?")
# broken_pattern = re.compile(r"#+")

def task1():
    with open(input_file) as input:
        result = 0
        i = 0
        for line in input:
            line = line.rstrip()
            pattern = tuple(map(int, re.findall(r"\d+", line)))
            springs = line.split(" ")[0]
            result += process(springs, pattern)
        return result


def task2():
    with open(input_file) as input:
        result = 0
        i = 0
        for line in input:
            line = line.rstrip()
            pattern = tuple(map(int, re.findall(r"\d+", line)))
            springs = line.split(" ")[0]
            pattern = pattern * 5
            springs = "?".join([springs] * 5)
            result += process(springs, pattern)
        return result

@cache
def process(springs, pattern):
    if len(springs) == 0 and len(pattern) == 0:
        return 1
    elif len(springs) == 0:
        return 0
    
    match springs[0]:
        case ".":
            return process(springs[1:], pattern)
        case "#":
            if len(pattern) == 0:
                return 0

            if len(springs) < pattern[0]:
                return 0

            expected_working = pattern[0]

            if "." in springs[:expected_working]:
                return 0

            if springs[expected_working:].startswith("#"):
                return 0
            
            if springs[expected_working:].startswith("?"):
                return process("." + springs[expected_working + 1:], pattern[1:])
            
            return process(springs[expected_working:], pattern[1:])
        case "?":
            return process(springs[1:], pattern) + process("#" + springs[1:], pattern)

# Bruteforce task 1 solution
# def get_combinations(line):
#     locations = tuple(m.start(0) for m in unknown_pattern.finditer(line))
#     location_combinations = tuple(itertools.chain.from_iterable(itertools.combinations(locations, r) for r in range(len(locations)+1)))
#     combinations = []
#     for location_combination in location_combinations:
#         combination = list(line)
#         for i in location_combination:
#             combination[i] = "#"
#         combination = list(map(lambda x: x.replace("?", "."), combination))
#         combinations.append(combination)
#     return tuple("".join(combination) for combination in combinations)

# def check_combination(combination, pattern):
#     combination_pattern = tuple(m.end() - m.start() for m in broken_pattern.finditer(combination))
#     return combination_pattern == pattern

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()