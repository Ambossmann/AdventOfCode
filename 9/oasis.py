import re
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    with open(input_file) as input:
        result = 0
        for line in input:
            sequences = []
            sequences.append(list(map(int, re.findall(r"-?\d+", line))))
            while any(v != 0 for v in sequences[-1]):
                sequence = []
                for i in range(len(sequences[-1])-1):
                    sequence.append(sequences[-1][i+1]-sequences[-1][i])
                sequences.append(sequence)
            sequences[-1].append(0)
            for i in range(len(sequences)-2, -1, -1):
                sequences[i].append(sequences[i][-1] + sequences[i+1][-1])
            result += sequences[0][-1]
        return result

def task2():
    with open(input_file) as input:
        result = 0
        for line in input:
            sequences = []
            sequences.append(list(map(int, re.findall(r"-?\d+", line))))
            while any(v != 0 for v in sequences[-1]):
                sequence = []
                for i in range(len(sequences[-1])-1):
                    sequence.append(sequences[-1][i+1]-sequences[-1][i])
                sequences.append(sequence)
            sequences[-1].insert(0, 0)
            for i in range(len(sequences)-2, -1, -1):
                sequences[i].insert(0, sequences[i][0] - sequences[i+1][0])
            result += sequences[0][0]
        return result

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()