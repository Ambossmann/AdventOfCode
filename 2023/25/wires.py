import os
import re
from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    graph = load_input()

    #Just determined the connecting edges by plotting the graph
    graph.remove_edge("htb", "bbg")
    graph.remove_edge("pjj", "dlk")
    graph.remove_edge("pcc", "htj")

    # plt.subplot(121)
    # nx.draw(graph, with_labels=True)
    # plt.show()

    sizes = [len(c) for c in nx.connected_components(graph)]

    return sizes[0] * sizes[1]

def task2():
    pass

def valid_coords(coords, grid):
    return 0 <= coords[0] < len(grid) and 0 <= coords[1] < len(grid[0]) 

def load_input():
    graph = nx.Graph()
    with open(input_file) as input:
        for line in input.read().splitlines():
            wires = re.findall(r"[a-z]+", line)
            for i in range(1, len(wires)):
                graph.add_edge(wires[0], wires[i])

    return graph

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()