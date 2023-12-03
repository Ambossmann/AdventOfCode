import re
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    result = 0
    with open(input_file) as input:
        text = input.read()
        length = len(text.splitlines()[0]) + 1
        for match in re.finditer(r"[0-9]+", text):
            around = [match.start() - 1, match.end()]
            for i in range(match.start() - 1, match.end() + 1):
                around.append(i - length)
                around.append(i + length)
            around.sort()
            around = tuple(filter(lambda i: i >= 0 and i < len(text), around))
            if any(text[i] not in ('.', '\n') + tuple(range(0, 10)) for i in around):
                result += int(match.group())
    return result

def task2():
    result = 0
    gears = dict()
    with open(input_file) as input:
        text = input.read()
        length = len(text.splitlines()[0]) + 1
        for match in re.finditer(r"[0-9]+", text):
            around = [match.start() - 1, match.end()]
            for i in range(match.start() - 1, match.end() + 1):
                around.append(i - length)
                around.append(i + length)
            around.sort()
            around = tuple(filter(lambda i: i >= 0 and i < len(text) and text[i] == '*', around))
            for i in around:
                if not i in gears.keys():
                    gears[i] = []
                gears[i].append(int(match.group()))
    for value in gears.values():
        if len(value) == 2:
            result += value[0] * value[1]
    return result

def main():
    print(task2())    

if __name__ == "__main__":
    main()