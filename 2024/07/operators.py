import os
import re
import itertools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    equations = load_input()
    result = 0
    for expected_result, inputs in equations:
        variations = itertools.product("*+", repeat=len(inputs) - 1)
        for variation in variations:
            actual_result = inputs[0]
            for i, operator in enumerate(variation):
                match operator:
                    case "*":
                        actual_result *= inputs[i + 1]
                    case "+":
                        actual_result += inputs[i + 1]
                if actual_result > expected_result:
                    break
            if actual_result == expected_result:
                result += expected_result
                break
    return result


def task2():
    equations = load_input()
    result = 0
    for expected_result, inputs in equations:
        variations = itertools.product("*+|", repeat=len(inputs) - 1)
        for variation in variations:
            actual_result = inputs[0]
            for i, operator in enumerate(variation):
                match operator:
                    case "*":
                        actual_result *= inputs[i + 1]
                    case "+":
                        actual_result += inputs[i + 1]
                    case "|":
                        actual_result = int(str(actual_result) + str(inputs[i + 1]))
                if actual_result > expected_result:
                    break
            if actual_result == expected_result:
                result += expected_result
                break
    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return tuple(
            map(
                lambda x: (int(x[0]), tuple(int(i) for i in x[1].split())),
                re.findall(r"(\d+): ((?:\d+ )+\d+)", inp.read()),
            )
        )


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
