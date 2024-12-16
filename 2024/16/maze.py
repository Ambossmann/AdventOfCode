import os
import time
from datetime import timedelta
from enum import Enum
from queue import Queue

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

    def turn_90_right(self):
        match self:
            case self.NORTH:
                result = self.EAST
            case self.SOUTH:
                result = self.WEST
            case self.WEST:
                result = self.NORTH
            case self.EAST:
                result = self.SOUTH
        return result

    def reverse(self):
        match self:
            case self.NORTH:
                result = self.SOUTH
            case self.SOUTH:
                result = self.NORTH
            case self.WEST:
                result = self.EAST
            case self.EAST:
                result = self.WEST
        return result

    def add_to_pos(self, pos):
        return (pos[0] + self.value[0], pos[1] + self.value[1])

    def __str__(self):
        match self:
            case self.NORTH:
                result = "NORTH"
            case self.SOUTH:
                result = "SOUTH"
            case self.WEST:
                result = "WEST"
            case self.EAST:
                result = "EAST"
        return result


NORTH_SOUTH = (Direction.NORTH, Direction.SOUTH)
WEST_EAST = (Direction.WEST, Direction.EAST)


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def in_bounds_pos(grid, pos):
    return in_bounds(grid, pos[0], pos[1])


def task1():
    graph, start_pos, end_pos = load_input()

    return nx.dijkstra_path_length(graph, (start_pos, WEST_EAST), (end_pos, None))


def positions_between(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    return [(i, j) for i in range(x1, x2 + 1) for j in range(y1, y2 + 1)]


def task2():
    graph, start_pos, end_pos = load_input()

    distance = {}
    predecessors = {}
    nodes = set()
    visited = set()

    start_node = (start_pos, WEST_EAST)
    predecessors[start_node] = set()
    nodes.add(start_node)
    distance[start_node] = 0

    while nodes:
        node = min(nodes, key=distance.get)
        nodes.remove(node)
        visited.add(node)
        for neighbor in nx.neighbors(graph, node):
            if neighbor not in visited:
                weight = graph[node][neighbor]["weight"]
                new_neighbor_distance = distance[node] + weight
                if neighbor not in distance or distance[neighbor] > new_neighbor_distance:
                    nodes.add(neighbor)
                    distance[neighbor] = new_neighbor_distance
                    predecessors[neighbor] = predecessors[node].union(
                        positions_between(node[0], neighbor[0])
                    )
                elif distance[neighbor] == new_neighbor_distance:
                    predecessors[neighbor].update(
                        predecessors[node].union(positions_between(node[0], neighbor[0]))
                    )

        if node == (end_pos, None):
            break

    return len(predecessors[(end_pos, None)])


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        graph = nx.Graph()

        junctions = {}
        reached_junctions = set()

        nodes = Queue()

        for i, line in enumerate(grid):

            for j, v in enumerate(line):
                if v != "#":
                    directions = set()
                    for d in Direction:
                        new_pos = d.add_to_pos((i, j))
                        if in_bounds_pos(grid, new_pos) and grid[new_pos[0]][new_pos[1]] != "#":
                            directions.add(d)
                    if (
                        len(directions) >= 2
                        and directions.intersection(NORTH_SOUTH)
                        and directions.intersection(WEST_EAST)
                    ):
                        junctions[(i, j)] = directions
                    if v == "S":
                        start_pos = (i, j)
                        if start_pos not in junctions:
                            junctions[start_pos] = set(d for d in Direction)
                        nodes.put(start_pos)

                    if v == "E":
                        end_pos = (i, j)
                        if end_pos not in junctions:
                            junctions[end_pos] = set(d for d in Direction)

        while not nodes.empty():
            pos = nodes.get()
            directions = junctions[pos]

            for d in directions:
                new_pos = d.add_to_pos(pos)
                l = 1
                while in_bounds_pos(grid, new_pos) and grid[new_pos[0]][new_pos[1]] != "#":
                    if new_pos in junctions:
                        if new_pos not in reached_junctions:
                            dir_set = NORTH_SOUTH if d in NORTH_SOUTH else WEST_EAST
                            graph.add_edge((pos, dir_set), (new_pos, dir_set), weight=l)
                            nodes.put(new_pos)
                        break
                    l += 1
                    new_pos = d.add_to_pos(new_pos)
            graph.add_edge((pos, NORTH_SOUTH), (pos, WEST_EAST), weight=1000)
            reached_junctions.add(pos)

        graph.add_edge((end_pos, NORTH_SOUTH), (end_pos, None), weight=0)
        graph.add_edge((end_pos, WEST_EAST), (end_pos, None), weight=0)

        return graph, start_pos, end_pos


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
