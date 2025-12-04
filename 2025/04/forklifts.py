import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def removable_rolls(grid):
    removable_roll_list = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "@":
                continue
            around = 0
            for a in range(-1, 2):
                for b in range(-1, 2):
                    if a == 0 and b == 0:
                        continue
                    if in_bounds(grid, i + a, j + b) and grid[i + a][j + b] == "@":
                        around += 1
            if around < 4:
                removable_roll_list.append((i, j))
    return removable_roll_list


def task1():
    grid = load_input()
    return len(removable_rolls(grid))


def task2():
    grid = load_input()
    removed_rolls = 0
    while rolls_to_remove := removable_rolls(grid):
        removed_rolls += len(rolls_to_remove)
        for i, j in rolls_to_remove:
            grid[i][j] = "."
    return removed_rolls


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        return grid


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
