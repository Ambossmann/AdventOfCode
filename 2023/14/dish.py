import os
import re
from functools import cache

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    rocks = load_rocks()

    roll_north(rocks)
    
    load = calculate_load(rocks)

    return load

def task2():
    rocks = load_rocks()

    steps = []

    number_of_steps = 1000000000
    for i in range(number_of_steps):
        rocks = spin(rocks)
        if (rocks in steps):
            last_index = steps.index(rocks)
            cycle_length = i - last_index
            last_cycle_start = number_of_steps - ((number_of_steps - last_index) % cycle_length)
            last_cycle_length = number_of_steps - last_cycle_start - 1
            rocks = steps[last_index + last_cycle_length]
            break
        steps.append(rocks)
    
    load = calculate_load(rocks)

    return load

def load_rocks():
    with open(input_file) as input:
        return input.read()

def parse_rocks(rocks_string):
    rocks = []
    for line in rocks_string.splitlines():
        rocks.append(re.findall(r"[#\.O]", line))
    return rocks

def calculate_load(rocks_string):
    rocks = parse_rocks(rocks_string)

    load = 0
    rock_length = len(rocks)
    for i in range(rock_length):
        load += rocks[i].count("O") * (rock_length - i)
    return load

@cache
def spin(rocks):
    rocks = roll_north(rocks)
    rocks = roll_west(rocks)
    rocks = roll_south(rocks)
    rocks = roll_east(rocks)
    return rocks

@cache
def roll_north(rocks_string):
    rocks = parse_rocks(rocks_string)

    for i in range(len(rocks)):
        for j in range(len(rocks[0])):
            if rocks[i][j] == "O":
                k = i - 1
                while k >= 0 and rocks[k][j] == ".":
                    k -= 1
                rocks[i][j] = "."
                rocks[k + 1][j] = "O"
    
    return "\n".join("".join(rock) for rock in rocks)

@cache
def roll_south(rocks_string):
    rocks = parse_rocks(rocks_string)

    for i in range(len(rocks) - 1, -1, -1):
        for j in range(len(rocks[0])):
            if rocks[i][j] == "O":
                k = i + 1
                while k < len(rocks) and rocks[k][j] == ".":
                    k += 1
                rocks[i][j] = "."
                rocks[k - 1][j] = "O"
    
    return "\n".join("".join(rock) for rock in rocks)

@cache
def roll_west(rocks_string):
    rocks = parse_rocks(rocks_string)

    for i in range(len(rocks[0])):
        for j in range(len(rocks)):
            if rocks[j][i] == "O":
                k = i - 1
                while k >= 0 and rocks[j][k] == ".":
                    k -= 1
                rocks[j][i] = "."
                rocks[j][k + 1] = "O"
    
    return "\n".join("".join(rock) for rock in rocks)

@cache
def roll_east(rocks_string):
    rocks = parse_rocks(rocks_string)

    for i in range(len(rocks[0]) - 1, -1, -1):
        for j in range(len(rocks)):
            if rocks[j][i] == "O":
                k = i + 1
                while k < len(rocks[0]) and rocks[j][k] == ".":
                    k += 1
                rocks[j][i] = "."
                rocks[j][k - 1] = "O"
    
    return "\n".join("".join(rock) for rock in rocks)

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()