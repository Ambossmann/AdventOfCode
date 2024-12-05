import os
import re


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    ordering_rules, updates = load_input()

    result = 0
    for update in updates:
        page_pairs = tuple(zip(update[:-1], update[1:]))
        if all(map(lambda x: x in ordering_rules, page_pairs)):
            result += update[int(len(update) / 2)]

    return result


def task2():
    ordering_rules, updates = load_input()

    result = 0
    for update in updates:
        page_pairs = tuple(zip(update[:-1], update[1:]))
        if not all(map(lambda x: x in ordering_rules, page_pairs)):
            update = list(update)
            for i in range(len(update)):
                for j in range(len(update) - i - 1):
                    if (update[j], update[j + 1]) not in ordering_rules:
                        tmp = update[j]
                        update[j] = update[j + 1]
                        update[j + 1] = tmp
            result += update[int(len(update) / 2)]

    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        text = inp.read()
        ordering_rules = tuple(
            map(
                lambda x: (int(x[0]), int(x[1])),
                re.findall(r"(\d+)\|(\d+)", text),
            )
        )
        updates = tuple(
            map(lambda x: tuple(map(int, x.split(","))), re.findall(r"(?:\d+,)+\d+", text))
        )
        return ordering_rules, updates


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
