import os
import re
import time
from datetime import timedelta
from queue import Queue

import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")


def run(gates, graph, wires):
    queue = Queue()

    for gate in gates:
        if all(graph.nodes[p]["value"] is not None for p in graph.predecessors(gate)):
            queue.put(gate)

    while not queue.empty():
        gate = queue.get()
        w1, w2 = graph.predecessors(gate)
        for w3 in graph.successors(gate):
            break
        else:
            raise AssertionError
        w1_value = graph.nodes[w1]["value"]
        w2_value = graph.nodes[w2]["value"]

        match graph.nodes[gate]["type"]:
            case "XOR":
                w3_value = w1_value ^ w2_value
            case "AND":
                w3_value = w1_value & w2_value
            case "OR":
                w3_value = w1_value | w2_value
            case _:
                raise ValueError
        graph.nodes[w3]["value"] = w3_value

        for gate in graph.successors(w3):
            if all(graph.nodes[p]["value"] is not None for p in graph.predecessors(gate)):
                queue.put(gate)

    z_values = list(
        map(
            lambda x: graph.nodes[x]["value"],
            reversed(sorted(filter(lambda x: x.startswith("z"), wires))),
        )
    )

    result = 0
    for z in z_values:
        result <<= 1
        result |= z

    return result


def task1():
    graph, gates, wires = load_input()

    return run(gates, graph, wires)


def task2():
    graph, _, _ = load_input()

    # Manually find problems by looking at graphviz
    nx.nx_agraph.write_dot(graph, os.path.join(__location__, "graph.dot"))
    return ",".join(sorted(("z17", "cmv", "rmj", "z23", "rdg", "z30", "mwp", "btb")))


def load_input():
    with open(input_file, encoding="utf-8") as inp:
        graph = nx.DiGraph()

        start_text, gate_text = inp.read().split("\n\n")

        wires = set()
        gates = set()

        for gate in re.findall(r"([^ \n]+) (XOR|AND|OR) ([^ ]+) -> ([^ \n]+)", gate_text):
            gate_name = f"{gate[1]}_{gate[0]}_{gate[2]}_{gate[3]}"
            graph.add_edge(gate[0], gate_name)
            graph.add_edge(gate[2], gate_name)
            graph.add_edge(gate_name, gate[3])
            graph.nodes[gate_name]["type"] = gate[1]
            gates.add(gate_name)
            wires.add(gate[0])
            wires.add(gate[2])
            wires.add(gate[3])

        # for gate in gates:
        #     graph.nodes[gate]["executed"] = False

        for wire in wires:
            graph.nodes[wire]["value"] = None

        for line in start_text.splitlines():
            wire, value = line.split(": ")
            graph.nodes[wire]["value"] = int(value)

        return graph, gates, wires


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
