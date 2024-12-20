import os
import time
from datetime import timedelta
from enum import Enum

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

    def add_to_pos(self, pos):
        return (pos[0] + self.value[0], pos[1] + self.value[1])


def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def in_bounds_pos(grid, pos):
    return in_bounds(grid, pos[0], pos[1])


def possible_offsets(cheat_duration):
    offsets = set()
    offsets.add((0, 0))
    for _ in range(cheat_duration):
        offset_copy = offsets.copy()
        for o in offset_copy:
            for d in Direction:
                offsets.add(d.add_to_pos(o))
    return offsets


def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def find_all_cheats(max_cheat_duration, min_save):
    graph, start_pos, end_pos = load_input()

    paths: dict = nx.single_target_shortest_path(graph, end_pos)

    result = 0

    offsets = possible_offsets(max_cheat_duration)

    for pos, path in paths.items():
        if pos in paths[start_pos]:
            for offset in offsets:
                cheat_end_pos = (pos[0] + offset[0], pos[1] + offset[1])
                if cheat_end_pos in graph:
                    if (
                        len(path) - (len(paths[cheat_end_pos]) + distance(pos, cheat_end_pos))
                        >= min_save
                    ):
                        result += 1

    return result


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        grid = list(map(lambda x: list(x.strip()), inp.readlines()))
        graph = nx.Graph()

        start_pos = None
        end_pos = None

        for i, line in enumerate(grid):
            for j, v in enumerate(line):
                if v != "#":
                    pos = (i, j)
                    for d in Direction:
                        new_pos = d.add_to_pos(pos)
                        if in_bounds_pos(grid, new_pos) and grid[new_pos[0]][new_pos[1]] != "#":
                            graph.add_edge(pos, new_pos)
                    if v == "S":
                        start_pos = pos

                    if v == "E":
                        end_pos = pos

        if start_pos is None or end_pos is None:
            raise RuntimeError("start or end not found")

        return graph, start_pos, end_pos


def main():
    start = time.perf_counter()
    task1_output = find_all_cheats(2, 100)
    end = time.perf_counter()
    print(f"Task 1: Result: {task1_output} Execution time: {timedelta(seconds=end-start)}")

    start = time.perf_counter()
    task2_output = find_all_cheats(20, 100)
    end = time.perf_counter()
    print(f"Task 2: Result: {task2_output} Execution time: {timedelta(seconds=end-start)}")


if __name__ == "__main__":
    main()
