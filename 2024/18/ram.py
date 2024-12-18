import os
import time
from datetime import timedelta

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def task1():
    graph, start_pos, end_pos, b = load_input()

    graph.remove_nodes_from(b[:1024])

    return nx.dijkstra_path_length(graph, start_pos, end_pos)


def task2():
    graph, start_pos, end_pos, by = load_input()
    for b in by:
        graph.remove_node(b)
        if not nx.has_path(graph, start_pos, end_pos):
            return f"{b[0]},{b[1]}"


def load_input():
    size = 71 # This needs to be changed accordingly when using the the test input
    with open(input_file, encoding="utf-8") as inp:
        graph = nx.grid_2d_graph(size, size)

        b = list(
            map(lambda x: tuple(map(int, x)), (line.strip().split(",") for line in inp.readlines()))
        )

        return graph, (0, 0), (size - 1, size - 1), b


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
