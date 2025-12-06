import os
from functools import reduce
from operator import mul

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    math = load_input1()
    result = 0
    for problem in math:
        match problem[-1]:
            case "+":
                result += sum(problem[:-1])
            case "*":
                result += reduce(mul, problem[:-1])
    return result


def task2():
    math = load_input2()
    result = 0
    for numbers, op in math:
        match op:
            case "+":
                result += sum(numbers)
            case "*":
                result += reduce(mul, numbers)
    return result


def load_input1():
    with open(input_file, encoding="utf-8") as inp:
        lines = list(map(str.split, inp.readlines()))
        for i in range(len(lines) - 1):
            lines[i] = list(map(int, lines[i]))
        return list(zip(*lines))


def load_input2():
    with open(input_file, encoding="utf-8") as inp:
        lines = inp.read().splitlines()
        columns = list(zip(*(map(iter, lines))))
        problems = []
        numbers = []
        curop = ""
        for c in columns:
            number = "".join(c[:-1]).replace(" ", "")
            if number == "":
                problems.append((numbers, curop))
                numbers = []
                continue
            number = int(number)
            numbers.append(number)
            if c[-1] != " ":
                curop = c[-1]
        problems.append((numbers, curop))
        return problems


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
