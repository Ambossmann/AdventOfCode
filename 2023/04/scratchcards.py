import re
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    result = 0
    with open(input_file) as input:
        for line in input:
            value = 0
            numbers = line.split(":")[1].split("|")
            winning_numbers = re.findall("[0-9]+", numbers[0])
            your_numbers = re.findall("[0-9]+", numbers[1])
            for i in your_numbers:
                if i in winning_numbers:
                    if value == 0:
                        value = 1
                    else:
                        value *= 2
            result += value
    return result

def task2():
    with open(input_file) as input:
        lines = input.readlines()
        count = []
        length = len(lines)
        for i in range(1, length+1):
            count.append(1)
        for line in lines:
            value = 0
            id = int(re.findall("Card +([0-9]+):", line)[0])
            numbers = line.split(":")[1].split("|")
            winning_numbers = re.findall("[0-9]+", numbers[0])
            your_numbers = re.findall("[0-9]+", numbers[1])
            for i in your_numbers:
                if i in winning_numbers:
                    value += 1
            for i in range(0, value):
                if i <= length:
                    count[id+i] += count[id-1]
    return sum(count)

def main():
    print(task2())

if __name__ == "__main__":
    main()