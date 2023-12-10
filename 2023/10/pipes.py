import re
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def task1():
    with open(input_file) as input:
        text = input.read()
        width = len(text.splitlines()[0].rstrip())
        pieces = re.findall(r"[^\n]", text)
        steps = 1
        index = pieces.index("S")
        if pieces[index-1] in ("-", "L", "F"):
            index = index - 1
            direction = LEFT
        elif pieces[index+1] in ("-", "J", "7"):
            index = index + 1
            direction = RIGHT
        elif pieces[index-width] in ("|", "7", "F"):
            index = index - width
            direction = UP
        elif pieces[index+width] in ("|", "L", "J"):
            index = index + width
            direction = DOWN
        while pieces[index] != "S":
            if pieces[index] == "|":
                if direction == UP:
                    index -= width
                else:
                    index += width
            elif pieces[index] == "-":
                if direction == RIGHT:
                    index += 1
                else:
                    index -= 1
            elif pieces[index] == "L":
                if direction == DOWN:
                    index += 1
                    direction = RIGHT
                else:
                    index -= width
                    direction = UP
            elif pieces[index] == "J":
                if direction == RIGHT:
                    index -= width
                    direction = UP
                else:
                    index -= 1
                    direction = LEFT
            elif pieces[index] == "7":
                if direction == RIGHT:
                    index += width
                    direction = DOWN
                else:
                    index -= 1
                    direction = LEFT
            elif pieces[index] == "F":
                if direction == UP:
                    index += 1
                    direction = RIGHT
                else:
                    index += width
                    direction = DOWN
            steps += 1
        return math.ceil(steps/2)

def task2():
    with open(input_file) as input:
        text = input.read()
        width = len(text.splitlines()[0].rstrip())
        pieces = re.findall(r"[^\n]", text)
        steps = 1
        index = pieces.index("S")
        loop = [0 for i in range(len(pieces))]
        loop[index] = 1
        if pieces[index-1] in ("-", "L", "F"):
            index = index - 1
            direction = LEFT
        elif pieces[index+1] in ("-", "J", "7"):
            index = index + 1
            direction = RIGHT
        elif pieces[index-width] in ("|", "7", "F"):
            index = index - width
            direction = UP
        elif pieces[index+width] in ("|", "L", "J"):
            index = index + width
            direction = DOWN
        while pieces[index] != "S":
            loop[index] = 1
            if pieces[index] == "|":
                if direction == UP:
                    index -= width
                else:
                    index += width
            elif pieces[index] == "-":
                if direction == RIGHT:
                    index += 1
                else:
                    index -= 1
            elif pieces[index] == "L":
                if direction == DOWN:
                    index += 1
                    direction = RIGHT
                else:
                    index -= width
                    direction = UP
            elif pieces[index] == "J":
                if direction == RIGHT:
                    index -= width
                    direction = UP
                else:
                    index -= 1
                    direction = LEFT
            elif pieces[index] == "7":
                if direction == RIGHT:
                    index += width
                    direction = DOWN
                else:
                    index -= 1
                    direction = LEFT
            elif pieces[index] == "F":
                if direction == UP:
                    index += 1
                    direction = RIGHT
                else:
                    index += width
                    direction = DOWN

        enclosed = [0 for i in range(len(loop))]
        for i in range(len(text.splitlines())):
            loop_encounters = 0
            for j in range(width):
                index = i * width + j
                if pieces[index] in ("|", "J", "L") and loop[index] == 1:
                        loop_encounters += 1
                else:
                    if loop_encounters % 2 == 1 and loop[index] == 0:
                        enclosed[index] = 1

        return enclosed.count(1)

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()