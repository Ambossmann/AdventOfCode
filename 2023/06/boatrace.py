import re
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    with open(input_file) as input:
        times = tuple(map(int, re.findall("\d+", input.readline())))
        distances = tuple(map(int, re.findall("\d+", input.readline())))
        races = tuple(zip(times, distances))
        result = 1
        for race in races:
            time, distance = race
            ways_to_win = 0
            for i in range(time+1):
                reachable_distance = (time - i) * i
                if reachable_distance > distance:
                    ways_to_win += 1
            result *= ways_to_win
        return result

def task2():
    with open(input_file) as input:
        time = int("".join(re.findall("\d+", input.readline())))
        distance = int("".join(re.findall("\d+", input.readline())))
        ways_to_win = 0
        for i in range(time+1):
            reachable_distance = (time - i) * i
            if reachable_distance > distance:
                ways_to_win += 1
        return ways_to_win

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()