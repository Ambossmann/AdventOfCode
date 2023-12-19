import os
import re
from queue import Queue

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    workflows, parts = load_input()
    return process_parts(workflows, parts)

def task2():
    workflows, _ = load_input()
    return process_range(1, 4000, workflows)

def process_parts(workflows, parts):

    accepted = []

    for part in parts:
        workflow_name = "in"
        while workflow_name not in ("A", "R"):
            workflow_name = process_part(workflows[workflow_name], part)
        else:
            if workflow_name == "A":
                accepted.append(part)
    
    return sum(sum(a) for a in accepted)

def process_part(workflow, part):
    for instruction in workflow[0]:
        value = part[instruction[0]]
        if check_condition(value, instruction[1], instruction[2]):
            return instruction[3]
    else:
        return workflow[1]

def check_condition(value, comparator, expected):
    if comparator:
        return value < expected
    else:
        return value > expected

def process_range(lower, upper, workflows):

    active_ranges = Queue()
    first = ((lower, upper), (lower, upper), (lower, upper), (lower, upper))

    accepted = []
    
    active_ranges.put(first)

    range_dict = {first: "in"}

    while not active_ranges.empty():
        active_range = active_ranges.get()
        key = range_dict[active_range]
        if key == "A":
            accepted.append(active_range)
            continue
        elif key == "R":
            continue
        workflow = workflows[key]
        for instruction in workflow[0]:
            variable = instruction[0]
            expected = instruction[2]
            if instruction[1]:
                if active_range[variable][1] >= expected:
                    if active_range[variable][0] < expected:
                        range1 = list(active_range)
                        range1[variable] = (active_range[variable][0], expected - 1)
                        range1 = tuple(range1)
                        active_range = list(active_range)
                        active_range[variable] = (expected, active_range[variable][1])
                        active_range = tuple(active_range)
                        active_ranges.put(range1)
                        range_dict[range1] = instruction[3]
                else:
                    active_ranges.put(active_range)
                    range_dict[active_range] = instruction[3]
                    break
            else:
                if active_range[variable][0] <= expected:
                    if active_range[variable][1] > expected:
                        range1 = list(active_range)
                        range1[variable] = (expected + 1, active_range[variable][1])
                        range1 = tuple(range1)
                        active_range = list(active_range)
                        active_range[variable] = (active_range[variable][0], expected)
                        active_range = tuple(active_range)
                        active_ranges.put(range1)
                        range_dict[range1] = instruction[3]
                else:
                    active_ranges.put(active_range)
                    range_dict[active_range] = instruction[3]
                    break
        else:
            active_ranges.put(active_range)
            range_dict[active_range] = workflow[1]
    
    result = 0
    for r in accepted:
        c = 1
        for i in r:
            c *= i[1] - i[0] + 1
        result += c
    return result

def load_input():
    workflows = {}
    parts = []
    with open(input_file) as input:
        text = input.read().splitlines()
        parsing_parts = False
        for line in text:
            if line == "":
                parsing_parts = True
                continue
            if parsing_parts:
                part = tuple(map(int, re.findall(r"\d+", line)))
                parts.append(part)
            else:
                description = re.findall(r"(?:([xmas])([<>])(\d+):([a-zAR]+))|([a-zAR]+)", line)
                name = description[0][4]
                working_descriptions = []
                for i in description:
                    if i[0] == "":
                        continue
                    match i[0]:
                        case "x":
                            variable = 0
                        case "m":
                            variable = 1
                        case "a":
                            variable = 2
                        case "s":
                            variable = 3
                    match i[1]:
                        case ">":
                            comparator = 0
                        case "<":
                            comparator = 1
                    expected = int(i[2])
                    resulting_workflow = i[3]
                    working_descriptions.append((variable, comparator, expected, resulting_workflow))
                end_workflow = description[-1][4]
                workflow = (tuple(working_descriptions), end_workflow)
                workflows[name] = workflow
    return workflows, tuple(parts)

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()