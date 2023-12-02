import re

def task1():
    maxCubes = (12, 13, 14)
    sum = 0
    with open("./2/input.txt", 'r') as input:
        for line in input:
            id = int(re.findall("Game ([0-9]+):", line)[0])
            draws = re.findall("[0-9]+ [a-z]+(?:, [0-9]+ [a-z]+)*", line)
            possible = True
            for draw in draws:
                rgb = parseDraw(draw)
                if any(x > y for x, y in zip(rgb, maxCubes)):
                    possible = False
            if possible:
                sum += id
    print(sum)

def task2():
    result = 0
    with open("./2/input.txt", 'r') as input:
        for line in input:
            id = int(re.findall("Game ([0-9]+):", line)[0])
            draws = re.findall("[0-9]+ [a-z]+(?:, [0-9]+ [a-z]+)*", line)
            minCubes = (0, 0, 0)
            for draw in draws:
                rgb = parseDraw(draw)
                minCubes = combineTuples(minCubes, rgb)
            result += minCubes[0]*minCubes[1]*minCubes[2]
    print(result)

def parseDraw(draw):
    red = re.findall("([0-9]+) red", draw)
    if red:
        red = int(red[0])
    else:
        red = 0
    green = re.findall("([0-9]+) green", draw)
    if green:
        green = int(green[0])
    else:
        green = 0
    blue = re.findall("([0-9]+) blue", draw)
    if blue:
        blue = int(blue[0])
    else:
        blue = 0
    return red, green, blue

def combineTuples(t1, t2):
    return tuple(t1[i] if t1[i] > t2[i] else t2[i] for i in range(len(t1)))

def main():
    task2()       

if __name__ == "__main__":
    main()