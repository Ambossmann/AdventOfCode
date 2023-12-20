import os
import re
from queue import Queue
import json
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    return process()

def task2():
    with open(input_file) as input:
        text = input.read()
        rx_input = re.findall(r"&([a-z]+) -> rx", text)[0]
        rx_input_input = re.findall(rf"&([a-z]+) -> {rx_input}", text)
    return math.lcm(*(find(x) for x in rx_input_input))

def process():
    connections, types, state = load_input()

    steps = []
    pulses = []

    number_of_steps = 1000
    for i in range(number_of_steps):
        encoded = json.dumps(state, sort_keys=True).encode()
        pulse, _ = process_button_press(connections, types, state)
        if (encoded in steps):
            last_index = steps.index(encoded)
            cycle = pulses[last_index:len(steps)+1]
            while (len(pulses) < number_of_steps):
                pulses += cycle
            break
        pulses.append(pulse)
        steps.append(encoded)
    
    low, high = zip(*pulses[:number_of_steps])
    return sum(low) * sum(high)

def find(target):
    connections, types, state = load_input()

    i = 1
    while not process_button_press(connections, types, state, target=target)[1]:
        i += 1
    return i

def process_button_press(connections, types, state, target=None):

    signals = Queue()
    sent = [1, 0]

    target_hit = False

    for c in connections["broadcaster"]:
        signals.put((c, 0, "broadcaster"))
        sent[0] += 1
    
    while not signals.empty():
        name, signal_type, sender = signals.get()
        if types[name]:
            if signal_type == 0:
                new_state = int(not state[name])
                state[name] = new_state
                for c in connections[name]:
                    if c in connections.keys():
                        signals.put((c, new_state, name))
                    sent[new_state] += 1
                    if (not new_state) and c == target:
                        target_hit = True
                    
        else:
            state[name][sender] = signal_type
            new_pulse = int(not all(state[name].values()))
            for c in connections[name]:
                if c in connections.keys():
                    signals.put((c, new_pulse, name))
                sent[new_pulse] += 1
                if (not new_pulse) and c == target:
                    target_hit = True
    
    return sent, target_hit

def load_input():
    connections = {}
    types = {}
    conjunction_inputs = {}
    state = []
    with open(input_file) as input:
        text = input.read().splitlines()
        for line in text:
            p = re.findall(r"[a-z]+", line)
            name = p[0]
            connected = p[1:]
            type = line[0]
            connections[name] = connected
            types[name] = type == "%"
        for name in connections.keys():
            for c in connections[name]:
                if c in connections.keys() and not types[c]:
                    inputs = conjunction_inputs.get(c, [])
                    inputs.append(name)
                    conjunction_inputs[c] = inputs
        
        for name in connections.keys():
            if types[name]:
                state.append((name, 0))
            elif name == "broadcaster":
                pass
            else:
                state.append((name, dict((x, 0) for x in conjunction_inputs[name])))

    return connections, types, dict(state)

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()