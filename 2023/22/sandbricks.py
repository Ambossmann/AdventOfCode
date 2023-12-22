import os
import re
from queue import Queue
import numpy as np
from operator import itemgetter
from queue import Queue

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    tower, supporting, supported_by = load_tower()
    max_brick = tower.max()

    result = 0
    for i in range(1, max_brick+1):
        for supported in supporting[i]:
            if len(supported_by[supported]) <= 1:
                break
        else:
            result += 1
    return result

def task2():
    tower, supporting, supported_by = load_tower()
    max_brick = tower.max()

    result = 0

    for brick in range(1, max_brick+1):
        queue = Queue()
        removed = set()

        queue.put(brick)
        removed.add(brick)

        while not queue.empty():
            current_brick = queue.get()

            for supported in supporting.get(current_brick, set()):
                if len(supported_by.get(supported, set) - removed) == 0:
                    removed.add(supported)
                    queue.put(supported)
        
        falling = len(removed) - 1
        result += falling

    return result

def load_tower():
    tower = np.zeros(shape=(400, 10, 10), dtype=np.int16)
    bricks = []
    with open(input_file) as input:
        text = input.read()
        for x in re.findall(r"(\d,\d,\d+)~(\d,\d,\d+)", text):
            values = tuple(tuple(map(int, y.split(","))) for y in x)
            x = min((values[0][0], values[1][0])), max(values[0][0], values[1][0])
            y = min((values[0][1], values[1][1])), max(values[0][1], values[1][1])
            z = min((values[0][2], values[1][2])), max(values[0][2], values[1][2])
            bricks.append((x, y, z))
        bricks.sort(key=itemgetter(2))
    
    height_indices = dict()
    
    for i in range(1, len(bricks) + 1):
        brick = bricks[i - 1]
        x, y, z = brick
        j = z[0]
        height = z[1] - z[0] + 1 
        x1 = x[0]
        x2 = x[1] + 1
        y1 = y[0]
        y2 = y[1] + 1
        while j >= 0:
            if j == 0:
                break
            disk = tower[j - 1, x1:x2, y1:y2]
            if np.count_nonzero(disk) > 0:
                break
            j -= 1
        j2 = j + height
        tower[j:j2, x1:x2, y1:y2] = i
        height_indices[i] = (j, j2 - 1)
    
    supporting = dict()
    supported_by = dict()
    for i in range(1, len(bricks) + 1):
        heighest_point = height_indices[i][1]
        disk = tower[heighest_point]
        indices = np.swapaxes(np.argwhere(disk==i), 0, 1)
        disk2 = tower[heighest_point+1]
        values = np.unique(disk2[indices[0], indices[1]])
        values = values[values != 0]
        supporting[i] = set(values)
        for j in supporting[i]:
            supported = supported_by.get(j, set())
            supported.add(i)
            supported_by[j] = supported

    return tower, supporting, supported_by

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()