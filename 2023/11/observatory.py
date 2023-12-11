import itertools
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    with open(input_file) as input:
        text = input.read()
        lines = text.splitlines()
        for i in range(len(lines)-1, -1, -1):
            if not "#" in lines[i]:
                lines.insert(i, lines[i])

        for i in range(len(lines[0])-1, -1, -1):
            if not "#" in (line[i] for line in lines):    
                for j in range(len(lines)-1, -1, -1):
                    lines[j] = f"{lines[j][:i]}.{lines[j][i:]}"

        galaxies = []

        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "#":
                    galaxies.append((i, j))
        
        combinations = itertools.combinations(galaxies, 2)

        result = 0

        for combination in combinations:
            distance = abs(combination[0][0]-combination[1][0]) + abs(combination[0][1]-combination[1][1])
            result += distance
        
        return result

def task2():
    with open(input_file) as input:
        text = input.read()
        lines = text.splitlines()

        horizontal_expansions = [0 for i in range(len(lines))]
        vertical_expansions = [0 for i in range(len(lines[0]))]
        expansion_strength = 1000000 - 1

        for i in range(len(lines)):
            if not "#" in lines[i]:
                horizontal_expansions[i] = 1

        for i in range(len(lines[0])):
            if not "#" in (line[i] for line in lines):
                vertical_expansions[i] = 1

        galaxies = []

        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "#":
                    galaxies.append((i + sum(horizontal_expansions[:i]) * expansion_strength, j + sum(vertical_expansions[:j]) * expansion_strength))
        
        combinations = itertools.combinations(galaxies, 2)

        result = 0

        for combination in combinations:
            distance = abs(combination[0][0]-combination[1][0]) + abs(combination[0][1]-combination[1][1])
            result += distance
        
        return result

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()