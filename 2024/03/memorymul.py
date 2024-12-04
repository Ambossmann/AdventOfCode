import os
import re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    muls = load_input_1()
    return sum(map(lambda x: x[0] * x[1], muls))


def task2():
    matches = load_input_2()
    print(matches)
    enabled = True
    result = 0
    for m in matches:
        if m[2]:
            enabled = True
        elif m[3]:
            enabled = False
        else:
            if enabled:
                result += int(m[0]) * int(m[1])
    return result



def load_input_1():
    with open(input_file, encoding="utf-8") as inp:
        return list(
            map(
                lambda x: (int(x[0]), int(x[1])),
                re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", inp.read()),
            )
        )

def load_input_2():
    with open(input_file, encoding="utf-8") as inp:
        return re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", inp.read())


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
