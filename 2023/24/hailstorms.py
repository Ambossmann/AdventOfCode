import os
import re
import itertools
import numpy as np
import sympy as sp

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    unique_combinations = tuple(itertools.combinations(load_input(), 2))
    result = 0
    area_min = 200000000000000
    area_max = 400000000000000
    for hailstorm1, hailstorm2 in unique_combinations:
        if intersects_in_area(hailstorm1, hailstorm2, area_min, area_max):
            result += 1
    return result

def task2():
    hailstorms = load_input()[:3]

    symbols = sp.symbols("p0 p1 p2 d0 d1 d2")
    p0, p1, p2, d0, d1, d2 = symbols

    equations = []
    for i in range(3):
        start, direction = hailstorms[i]
        t = sp.symbols(f"t{i}")
        symbols = symbols + tuple([t])
        equations.append(sp.Eq(p0 + t * d0, start[0] + t * direction[0]))
        equations.append(sp.Eq(p1 + t * d1, start[1] + t * direction[1]))
        equations.append(sp.Eq(p2 + t * d2, start[2] + t * direction[2]))
    
    return sum(sp.nonlinsolve(equations, symbols).args[0][:3])

def is_in_past(value, delta, start):
    return (delta > 0 and value <= start) or (delta < 0 and value >= start)

def intersects_in_area(a, b, area_min, area_max):
    x1 = a[0][0]
    y1 = a[0][1]
    x2 = x1 + a[1][0]
    y2 = y1 + a[1][1]
    x3 = b[0][0]
    y3 = b[0][1]
    x4 = x3 + b[1][0]
    y4 = y3 + b[1][1]

    denom = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    if denom == 0:
        return (x1 - x3) * a[1][1] - (y1 - y3) * a[1][0] == 0

    px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/denom

    py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/denom

    if is_in_past(px, a[1][0], x1) or is_in_past(py, a[1][1], y1) or is_in_past(px, b[1][0], x3) or is_in_past(py, b[1][1], y3):
        return False

    return area_max >= px >= area_min and area_max >= py >= area_min

def load_input():
    with open(input_file) as input:
        text = input.read()
        hailstorms = tuple(map(lambda x: (x[:3], x[3:]), (tuple(map(int, y)) for y in re.findall(r"(-?\d+), (-?\d+), (-?\d+) @ (-?\d+), (-?\d+), (-?\d+)", text))))

    return hailstorms

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()