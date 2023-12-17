import os
import re
import math
from queue import PriorityQueue

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)

def task1():
    city = load_city()
    return find_shortest(city, 0, 3)

def task2():
    city = load_city()
    return find_shortest(city, 3, 10)

def find_shortest(city, minimum_straight_line, maximum_straight_line):
    
    visited_blocks = set()

    corner_coords = (len(city) - 1, len(city[0]) - 1)

    current = PriorityQueue()

    current.put_nowait((city[0][1], ((0, 1), RIGHT, 0)))
    
    current.put_nowait((city[1][0], ((1, 0), DOWN, 0)))

    while not current.empty():
        current_data = current.get_nowait()
        current_block, current_direction, straight_line_count = current_data[1]
        current_value = current_data[0]

        if current_block == corner_coords and straight_line_count >= minimum_straight_line:
            return current_value
        
        if current_data[1] in visited_blocks:
            continue

        if straight_line_count < (maximum_straight_line - 1):
            straight_block = (current_block[0] + current_direction[0], current_block[1] + current_direction[1])
            if valid_coords(straight_block, city):
                new_value = current_value + city[straight_block[0]][straight_block[1]]
                new_data = (straight_block, current_direction, straight_line_count + 1)
                current.put_nowait((new_value, new_data))
        
        if straight_line_count >= minimum_straight_line:
            left_direction = (current_direction[1], -current_direction[0])
            left_block = (current_block[0] + left_direction[0], current_block[1] + left_direction[1])
            if valid_coords(left_block, city):
                new_value = current_value + city[left_block[0]][left_block[1]]
                new_data = (left_block, left_direction, 0)
                current.put_nowait((new_value, new_data))

            right_direction = (-current_direction[1], current_direction[0])
            right_block = (current_block[0] + right_direction[0], current_block[1] + right_direction[1])
            if valid_coords(right_block, city):
                new_value = current_value + city[right_block[0]][right_block[1]]
                new_data = (right_block, right_direction, 0)
                current.put_nowait((new_value, new_data))

        visited_blocks.add(current_data[1])
                        
def valid_coords(coords, city):
    return 0 <= coords[0] < len(city) and 0 <= coords[1] < len(city[0]) 

def load_city():
    with open(input_file) as input:
        text = input.read().splitlines()
        return list(list(map(int, re.findall(r"[^\n]", line))) for line in text)


def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()