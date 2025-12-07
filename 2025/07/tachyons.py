import os
from collections import Counter, deque

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def simulate_tachyon():
    start, grid, last_row = load_input()
    workset = deque()
    workset.append(start)
    timelines = Counter()
    timelines[start] = 1
    splits = 0
    total_timelines = 0
    while workset:
        (y, x) = workset.popleft()
        cur_timelines = timelines[(y, x)]
        if y != last_row:
            match grid[y + 1][x]:
                case ".":
                    if (y + 1, x) not in timelines:
                        workset.append((y + 1, x))
                    timelines[(y + 1, x)] += cur_timelines
                case "^":
                    splits += 1
                    if (y + 1, x - 1) not in timelines:
                        workset.append((y + 1, x - 1))
                    timelines[(y + 1, x - 1)] += cur_timelines
                    if (y + 1, x + 1) not in timelines:
                        workset.append((y + 1, x + 1))
                    timelines[(y + 1, x + 1)] += cur_timelines
                case _:
                    raise RuntimeError
        else:
            total_timelines += cur_timelines
    return splits, total_timelines


def task1():
    splits, _ = simulate_tachyon()
    return splits


def task2():
    _, total_timelines = simulate_tachyon()
    return total_timelines


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        start = (0, grid[0].index("S"))
        return start, grid, len(grid) - 1


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
