import os
from collections import Counter
from functools import cache

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def path_count(graph, source, target):
    num_paths = Counter()
    num_paths[source] = 1

    for node in nx.topological_sort(graph):
        if node == target:
            return num_paths[target]
        for d in graph.successors(node):
            num_paths[d] += num_paths[node]


def task1():
    graph = load_input()

    return path_count(graph, "you", "out")


def task2():
    graph = load_input()

    # The graph is a DAG, with only fft leading to dac
    return (
        path_count(graph, "svr", "fft")
        * path_count(graph, "fft", "dac")
        * path_count(graph, "dac", "out")
    )


@cache
def load_input():
    with open(input_file, encoding="utf-8") as inp:
        graph = nx.DiGraph()

        for line in inp.readlines():
            label, outputs = line.split(":")
            for output in outputs.split():
                graph.add_edge(label, output)

        return graph


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
