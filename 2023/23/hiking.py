import os
import re
from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)

DIRECTIONS = (RIGHT, DOWN, LEFT, UP)
DIRECTION_SLOPES = {RIGHT: ">", DOWN: "v", LEFT: "<", UP: "^"}

def task1():
    trails = load_input()

    start = (0, 1)
    end = (len(trails) - 1, len(trails[0]) - 2)

    nodes = Queue()
    nodes.put(start)

    graph = nx.DiGraph()

    while not nodes.empty():
        node = nodes.get()

        calculated = set()
        distance = dict()

        distance[node] = 1
        calculated.add(node)

        tiles = Queue()

        tiles.put(node)

        while not tiles.empty():
            tile = tiles.get()
            for d in DIRECTIONS:
                    new_tile = (tile[0] + d[0], tile[1] + d[1])
                    if valid_coords(new_tile, trails):
                        new_tile_type = trails[new_tile[0]][new_tile[1]]
                        if (not new_tile in calculated) and new_tile_type != "#":
                            if new_tile == end:
                                distance[new_tile] = distance[tile] + 1
                                calculated.add(new_tile)
                                graph.add_edge(node, new_tile, weight=distance[new_tile])
                            elif new_tile_type in DIRECTION_SLOPES.values():
                                if DIRECTION_SLOPES[d] == new_tile_type:
                                    distance[new_tile] = distance[tile] + 1
                                    calculated.add(new_tile)
                                    slope = (new_tile[0] + d[0], new_tile[1] + d[1])
                                    graph.add_edge(node, slope, weight=distance[new_tile])
                                    nodes.put(slope)
                            else:
                                distance[new_tile] = distance[tile] + 1
                                calculated.add(new_tile)
                                tiles.put(new_tile)
    
    return nx.dag_longest_path_length(graph) - 1

def task2():
    trails = load_input()

    start = (0, 1)
    end = (len(trails) - 1, len(trails[0]) - 2)

    nodes = Queue()
    nodes.put(start)

    graph = nx.Graph()

    junctions = set()

    for i in range(1, len(trails) - 1):
        for j in range (1, len(trails[0]) - 1):
            if trails[i][j] != "#":
                n = 0
                for d in DIRECTIONS:
                    if trails[i+d[0]][j+d[1]] != "#":
                        n += 1
                if n > 2:
                    junctions.add((i, j))
    reached_junctions = set()

    calculated = set()

    while not nodes.empty():
        node = nodes.get()

        distance = dict()


        distance[node] = 0

        tiles = Queue()

        tiles.put(node)

        while not tiles.empty():
            tile = tiles.get()
            if tile in junctions and distance[tile] > 0:
                graph.add_edge(node, tile, weight=distance[tile])
                if tile not in reached_junctions:
                    nodes.put(tile)
                reached_junctions.add(tile)
            else:
                neighbour = []
                for d in DIRECTIONS:
                    new_tile = (tile[0] + d[0], tile[1] + d[1])
                    if valid_coords(new_tile, trails):
                        new_tile_type = trails[new_tile[0]][new_tile[1]]
                        if new_tile_type != "#" and (new_tile not in calculated or new_tile in junctions):
                            neighbour.append(new_tile)
                for new_tile in neighbour:
                    if new_tile == end:
                        distance[new_tile] = distance[tile] + 1
                        graph.add_edge(node, new_tile, weight=distance[new_tile])
                    else:
                        distance[new_tile] = distance[tile] + 1
                        calculated.add(new_tile)
                        tiles.put(new_tile)

    graph.remove_edges_from(nx.selfloop_edges(graph))

    return max([(path, sum(graph.edges[pair]['weight'] for pair in list(nx.utils.pairwise(path)))) for path in nx.all_simple_paths(graph, start, end)], key=lambda x: x[1])[1]

def valid_coords(coords, grid):
    return 0 <= coords[0] < len(grid) and 0 <= coords[1] < len(grid[0]) 

def load_input():
    with open(input_file) as input:
        text = [[c for c in line] for line in input.read().splitlines()]

    return text

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()