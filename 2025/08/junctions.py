import os
import re
from functools import cache, reduce
from itertools import combinations, islice
from math import sqrt
from operator import mul

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def distance(a, b):
    return sqrt(sum(map(lambda x: (x[0] - x[1]) ** 2, zip(a, b))))


def task1():
    graph = load_input()

    mse = sorted(graph.edges.data(), key=lambda e: e[2]["weight"])

    mse = islice(mse, 1000)
    mse = set(map(lambda x: (x[0], x[1]), mse))
    reduced_graph = nx.subgraph_view(graph, filter_edge=nx.filters.show_edges(mse))

    cc = nx.connected_components(reduced_graph)
    return reduce(mul, map(len, islice(sorted(cc, key=len, reverse=True), 3)))


def task2():
    graph = load_input()

    mse = list(nx.minimum_spanning_edges(graph))

    last_edge = mse[-1]

    return last_edge[0][0] * last_edge[1][0]


@cache
def load_input():
    with open(input_file, encoding="utf-8") as inp:
        nodes = list(
            map(
                lambda x: (int(x[0]), int(x[1]), int(x[2])),
                re.findall(r"(\d+),(\d+),(\d+)", inp.read()),
            )
        )

        graph = nx.Graph()

        for a, b in combinations(nodes, 2):
            graph.add_edge(a, b, weight=distance(a, b))

        return graph


def main():
    print(task1())
    print(task2())


if __name__ == "__main__":
    main()
