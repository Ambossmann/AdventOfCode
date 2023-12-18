import os
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)

def task1():
    instructions = load_instructions()
    return dig_hole(instructions)

def task2():
    instructions = load_instructions(usehex=True)
    return dig_hole(instructions)

def dig_hole(instructions):
    #computes Area of the Polygon formed by the trenches as explained on https://www.wikihow.com/Calculate-the-Area-of-a-Polygon

    corners = []
    
    current = (0, 0)

    complete_length = 0

    corners.append(current)
    for instruction in instructions:
        direction, length = instruction
        current = tuple(sum(x) for x in zip(current, (length*y for y in direction)))
        corners.insert(0, current)
        complete_length += length
    
    part_result_1 = 0
    part_result_2 = 0
    for i in range(len(corners) - 1):
        part_result_1 += corners[i][0] * corners[i+1][1]
        part_result_2 += corners[i][1] * corners[i+1][0]
    
    #I Don't know why this works but it does
    return int((part_result_1 - part_result_2 + complete_length) / 2) + 1

def load_instructions(usehex=False):
    instructions = []
    with open(input_file) as input:
        for instruction in re.findall(r"([A-Z]) (\d+) \(#([\da-f]{6})\)", input.read()):
            if not usehex:
                match instruction[0]:
                    case "U":
                        direction = UP
                    case "R":
                        direction = RIGHT
                    case "D":
                        direction = DOWN
                    case "L":
                        direction = LEFT
                length = int(instruction[1])
            else:
                match instruction[2][-1]:
                    case "3":
                        direction = UP
                    case "0":
                        direction = RIGHT
                    case "1":
                        direction = DOWN
                    case "2":
                        direction = LEFT
                length = int(instruction[2][:5], base=16)
            instructions.append((direction, length))
    return instructions

def valid_coords(coords, grid):
    return 0 <= coords[0] < len(grid) and 0 <= coords[1] < len(grid[0]) 

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()