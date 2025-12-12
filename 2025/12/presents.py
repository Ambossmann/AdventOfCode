import os
import re
from functools import cache

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import CNFPlus, IDPool
from pysat.solvers import Gluecard4

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    polyminos, trees = load_input()

    solvable = 0

    polymino_sizes = tuple(np.sum(v) for v in polyminos.values())

    for i, (width, height, amounts) in enumerate(trees):
        min_area = sum(map(lambda x: x[0] * x[1], zip(polymino_sizes, amounts)))

        # More tiles would be needed than are available
        if min_area > width * height:
            continue

        # Presents can be trivially 3x3 tiled
        if sum(amounts) <= (width // 3) * (height // 3):
            solvable += 1
            continue

        # This part is sadly never used outside the example input.
        id_pool = IDPool()

        grid = tuple(tuple([] for _ in range(width)) for _ in range(height))
        polymino_possibilities = tuple([] for _ in range(len(polyminos)))

        for x in range(width - 2):
            for y in range(height - 2):
                for p in polyminos:
                    for r in range(4):
                        ident = id_pool.id((x, y, p, r))
                        polymino_possibilities[p].append(ident)
                        rotated = np.rot90(polyminos[p], k=r)
                        for x_2 in range(3):
                            for y_2 in range(3):
                                if rotated[y_2][x_2]:
                                    grid[y + y_2][x + x_2].append(ident)

        cnf = CNFPlus()
        for x in range(width):
            for y in range(height):
                cnf.extend(CardEnc.atmost(grid[y][x], vpool=id_pool, encoding=EncType.native))
        for p in polyminos:
            cnf.extend(
                CardEnc.equals(
                    polymino_possibilities[p], amounts[p], vpool=id_pool, encoding=EncType.native
                )
            )

        with Gluecard4(bootstrap_with=cnf, use_timer=True) as g:
            if g.solve():
                solvable += 1
            print(i, g.accu_time, g.accum_stats())
    return solvable


def task2():
    pass


@cache
def load_input():
    with open(input_file, encoding="utf-8") as inp:
        text = inp.read()

        polyminos = {}
        for p_id, polymino in re.findall(r"(\d+):\n((?:[.#]{3}\n){3})", text):
            matrix = np.asarray([[1 if c == "#" else 0 for c in s] for s in polymino.split()])
            polyminos[int(p_id)] = matrix

        trees = []
        for width, height, *amounts in map(
            lambda x: map(int, x), re.findall(r"(\d+)x(\d+):" + r" (\d+)" * len(polyminos), text)
        ):
            trees.append((width, height, tuple(amounts)))

        return polyminos, tuple(trees)


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
