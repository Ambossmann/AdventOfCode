import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    reports = load_input()
    result = 0
    for report in reports:
        sorted_report = tuple(sorted(report))
        if sorted_report == report or tuple(reversed(sorted_report)) == report:
            prev = sorted_report[0]
            for i in range(1, len(sorted_report)):
                current = sorted_report[i]
                diff = current - prev
                if diff < 1 or diff > 3:
                    break
                prev = current
            else:
                result += 1
    return result


def task2():
    reports = load_input()
    result = 0
    for report in reports:
        for i in range(-1, len(report)):
            if i == -1:
                changed_report = report
            else:
                changed_report = report[:i] + report[i + 1 :]
            sorted_report = tuple(sorted(changed_report))
            if sorted_report == changed_report or tuple(reversed(sorted_report)) == changed_report:
                prev = sorted_report[0]
                for i in range(1, len(sorted_report)):
                    current = sorted_report[i]
                    diff = current - prev
                    if diff < 1 or diff > 3:
                        break
                    prev = current
                else:
                    result += 1
                    break
    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        return tuple(map(lambda x: tuple(map(int, x.strip().split())), inp.readlines()))


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
