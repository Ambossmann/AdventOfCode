import os
import re
import time
from collections import deque
from datetime import timedelta

from scipy.optimize import linprog
from sympy import Add, Eq, linear_eq_to_matrix, matrix2numpy, solve, symbols
from sympy.utilities.misc import as_int

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    machines = load_input()

    total = 0

    for target, buttons, _ in machines:

        start = tuple(False for _ in range(len(target)))
        depth = {start: 0}
        queue = deque(depth)

        while queue:
            cur = queue.popleft()
            for b in buttons:
                new_state = tuple((not x if i in b else x) for i, x in enumerate(cur))
                if new_state not in depth:
                    depth[new_state] = depth[cur] + 1
                    queue.append(new_state)
                if cur == target:
                    break

        total += depth[target]

    return total


def task2():
    machines = load_input()

    total = 0

    for _, buttons, joltage in machines:

        syms = symbols(f"b0:{len(buttons)}", integer=True)
        equations = []
        for i, j in enumerate(joltage):
            used_buttons = []
            for k, b in enumerate(buttons):
                if i in b:
                    used_buttons.append(syms[k])
            equations.append(Eq(Add(*used_buttons), j))
        sol = solve(equations, syms, set=True)
        free_vars = set()
        for sol_expres in sol[1]:
            break
        for e in sol_expres:
            free_vars |= e.free_symbols
        free_vars = list(free_vars)

        sum_expr = Add(*sol_expres)

        if free_vars:
            c, _ = linear_eq_to_matrix(sum_expr, syms)
            a, b = linear_eq_to_matrix([-e for e in sol_expres], syms)
            # The equalities are needed to also constrain the non-free variables to integers
            equalities = []
            for i in range(len(syms)):
                if syms[i] not in free_vars:
                    equalities.append(Eq(syms[i], sol_expres[i]))
            aeq, beq = linear_eq_to_matrix(equalities, syms)
            c = matrix2numpy(c).flatten()
            a = matrix2numpy(a)
            b = matrix2numpy(b).flatten()
            aeq = matrix2numpy(aeq)
            beq = matrix2numpy(beq).flatten()
            # Use the scipy linprog because it supports constraining to integers
            min_sol = linprog(c, a, b, aeq, beq, method="highs", integrality=1)
            free_var_vals = {k: v for k, v in zip(syms, min_sol["x"])}
        else:
            free_var_vals = {}
        needed = as_int(sum_expr.evalf(subs=free_var_vals), strict=False)

        total += needed

    return total


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        machines = []
        for line in inp.readlines():
            target = tuple(x == "#" for x in re.match(r"\[([.#]*)\]", line).group(1))

            buttons = tuple(
                sorted(
                    (
                        tuple(int(i) for i in x.split(","))
                        for x in re.findall(r"\(([\d,]*)\)", line)
                    ),
                    key=len,
                    reverse=True,
                )
            )

            joltage = tuple(
                tuple(int(i) for i in re.search(r"{([\d,]*)}", line).group(1).split(","))
            )

            machines.append((target, buttons, joltage))

        return tuple(machines)


def main():
    start = time.perf_counter()
    task1_output = task1()
    end = time.perf_counter()
    print(f"Task 1: Result: {task1_output} Execution time: {timedelta(seconds=end-start)}")

    start = time.perf_counter()
    task2_output = task2()
    end = time.perf_counter()
    print(f"Task 2: Result: {task2_output} Execution time: {timedelta(seconds=end-start)}")


if __name__ == "__main__":
    main()
