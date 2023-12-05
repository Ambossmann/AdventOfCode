import re
import os
import time
import numpy as np

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    with open(input_file) as input:
        almanac = input.read()
        mappings = parse_mappings(almanac)
        seeds = list(map(int, re.findall("\d+", almanac.splitlines()[0])))
        return min(seed_to_location(mappings, s) for s in seeds)

def task2():
    with open(input_file) as input:
        almanac = input.read()
        mappings = parse_mappings(almanac)
        seed_pairs = tuple(map(int, re.findall("\d+", almanac.splitlines()[0])))

        array_length = 0xFFFF_FFFF

        m = np.arange(array_length, dtype=np.uint32)
        d = np.zeros(array_length, dtype=np.bool_)

        print("Arrays Created")

        i = 1
        for mapp in mappings:
            j = 1
            d.fill(False)
            for mapping in mapp:
                destination, source, length = mapping
                end = source + length
                offset = destination - source
                n = np.where((source <= m) & (m < end) & (d == False), m + offset, m)
                d = np.where((source <= m) & (m < end) & (d == False), True, d)
                m = n
                print(f"{i}.{j}: {m}")
                j += 1
            i += 1
        result = np.min(m[seed_pairs[0]:seed_pairs[0]+seed_pairs[1]])
        for i in range(2, len(seed_pairs), 2):
            j = np.min(m[seed_pairs[i]:seed_pairs[i]+seed_pairs[i+1]])
            result = j if j < result else result
        return result

def seed_to_location(mappings, seed):
    for m in mappings:
        done = False
        for mapping in m:
            destination, source, length = mapping
            offset = destination - source
            if seed >= source and seed < source + length and not done:
                seed = seed + offset
                done = True
            if done:
                break
    return seed

def parse_mappings(almanac):
    parsed_mappings = []
    maps = re.findall("\w+-to-\w+ map:\n(?:\d+ \d+ \d+\n)+", almanac)
    for m in maps:
        ma = []
        mappings = re.findall("\d+ \d+ \d+", m)
        for mapping in mappings:
            ma.append(tuple(map(int, mapping.split(" "))))
        parsed_mappings.append(ma)
    return parsed_mappings

def main():
    print(task2())

if __name__ == "__main__":
    main()