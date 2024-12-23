import os
import time
from datetime import timedelta

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    graph = load_input()

    result = 0

    # First naive implementation. About 100 times slower than the current one
    # for cycle in nx.simple_cycles(graph, length_bound=3):
    #     if any(n.startswith("t") for n in cycle):
    #         result += 1

    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) < 3:
            continue
        if len(clique) > 3:
            break
        if any(n.startswith("t") for n in clique):
            result += 1

    return result


def task2():
    graph = load_input()

    clique = []

    for c in nx.find_cliques(graph):
        if len(c) > len(clique):
            clique = c

    return ",".join(sorted(clique))


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        graph = nx.Graph()

        graph.add_edges_from(map(lambda x: x.split("-"), inp.read().splitlines()))

        return graph


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
