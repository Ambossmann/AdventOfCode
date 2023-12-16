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
    mirrors = load_mirrors()
    return simulate_beams(mirrors, (0, 0), RIGHT)

def task2():
    mirrors = load_mirrors()
    result = 0
    for i in range(len(mirrors)):
        result = max(result, simulate_beams(mirrors, (i, 0), RIGHT))
        result = max(result, simulate_beams(mirrors, (i, len(mirrors[0]) - 1), LEFT))
    for i in range(len(mirrors[0])):
        result = max(result, simulate_beams(mirrors, (0, i), DOWN))
        result = max(result, simulate_beams(mirrors, (0, len(mirrors) - 1), UP))
    return result
                
def simulate_beams(mirrors, start_coords, start_direction):
    tiles = [[[] for j in range(len(mirrors[0]))] for i in range(len(mirrors))]

    tiles[start_coords[0]][start_coords[1]].append(start_direction)

    beams = [(start_coords, start_direction)]

    while beams:
        for beam in beams:
            direction = beam[1]
            match mirrors[beam[0][0]][beam[0][1]]:
                case ".":
                    propgate_beam(mirrors, tiles, beams, beam, direction)

                case "-":
                    if direction in (LEFT, RIGHT):
                        propgate_beam(mirrors, tiles, beams, beam, direction)

                    else:
                        direction = LEFT
                        propgate_beam(mirrors, tiles, beams, beam, direction)
                        
                        direction = RIGHT
                        propgate_beam(mirrors, tiles, beams, beam, direction)

                case "|":
                    if direction in (UP, DOWN):
                        propgate_beam(mirrors, tiles, beams, beam, direction)

                    else:
                        direction = UP
                        propgate_beam(mirrors, tiles, beams, beam, direction)
                        
                        direction = DOWN
                        propgate_beam(mirrors, tiles, beams, beam, direction)
                
                case "\\":
                    if direction == RIGHT:
                        direction = DOWN
                    elif direction == DOWN:
                        direction = RIGHT
                    elif direction == LEFT:
                        direction = UP
                    elif direction == UP:
                        direction = LEFT

                    propgate_beam(mirrors, tiles, beams, beam, direction)

                case "/":
                    if direction == RIGHT:
                        direction = UP
                    elif direction == DOWN:
                        direction = LEFT
                    elif direction == LEFT:
                        direction = DOWN
                    elif direction == UP:
                        direction = RIGHT

                    propgate_beam(mirrors, tiles, beams, beam, direction)
            
            beams.remove(beam)
    
    result = 0

    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            if tiles[i][j]:
                result += 1

    return result
                        
def valid_coords(coords, mirrors):
    return 0 <= coords[0] < len(mirrors) and 0 <= coords[1] < len(mirrors[0])         

def propgate_beam(mirrors, tiles, beams, beam, direction):
    new_coords = tuple(sum(x) for x in zip(beam[0], direction))
    if valid_coords(new_coords, mirrors):
        if not direction in tiles[new_coords[0]][new_coords[1]]:
            beams.append((new_coords, direction))
            tiles[new_coords[0]][new_coords[1]].append(direction)

def load_mirrors():
    with open(input_file) as input:
        text = input.read().splitlines()
        return [re.findall(r"[^\n]", line) for line in text]


def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()