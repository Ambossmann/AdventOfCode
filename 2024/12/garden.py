import os
import time
from datetime import timedelta
from enum import Enum

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def turn_90_right(self):
        match self:
            case self.UP:
                result = self.RIGHT
            case self.DOWN:
                result = self.LEFT
            case self.LEFT:
                result = self.UP
            case self.RIGHT:
                result = self.DOWN
        return result

    def add_to_pos(self, pos):
        return (pos[0] + self.value[0], pos[1] + self.value[1])


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def in_bounds_pos(grid, pos):
    return in_bounds(grid, pos[0], pos[1])


def task1():
    graph = load_input()
    result = 0
    for component in nx.connected_components(graph):
        subgraph = graph.subgraph(component)
        area = subgraph.number_of_nodes()
        perimeter = 4 * area - 2 * subgraph.number_of_edges()

        result += area * perimeter

    return result


def task2():
    graph = load_input()
    result = 0
    for component in nx.connected_components(graph):
        subgraph = graph.subgraph(component).copy()

        area = subgraph.number_of_nodes()

        edges = 0

        for direction in Direction:
            positions = set()
            for node in subgraph.nodes:
                pos_plus_dir = direction.add_to_pos(node)
                if pos_plus_dir not in subgraph.nodes:
                    positions.add(pos_plus_dir)
            dir_right = direction.turn_90_right()
            real_positions = set()
            for position in positions:
                if dir_right.add_to_pos(position) not in positions:
                    real_positions.add(position)
            edges += len(real_positions)

        result += area * edges

    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        graph = nx.Graph()
        for i, line in enumerate(grid):
            for j, v in enumerate(line):
                graph.add_node((i, j), v=v)

        for i, line in enumerate(grid):
            for j, v in enumerate(line):
                for direction in Direction:
                    pos = (i, j)
                    x, y = neighbor_pos = direction.add_to_pos(pos)
                    if in_bounds_pos(grid, neighbor_pos):
                        neighbor_value = grid[x][y]
                        if neighbor_value == v:
                            graph.add_edge(pos, neighbor_pos)

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
