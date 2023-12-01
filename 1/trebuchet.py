import re

def task1():
    sum: int = 0
    with open("./1/input.txt", 'r') as input:
        for line in input:
            digits = re.findall("[0-9]", line)
            sum += int(digits[0] + digits[-1])
    print(sum)

def task2():
    sum = 0
    with open("./1/input.txt", 'r') as input:
        for line in input:
            digits = re.findall("(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", line)
            sum += int(parseNum(digits[0]) + parseNum(digits[-1]))
    print(sum)

def parseNum(num: str) -> str:
    result: int
    if num == "1" or num == "one":
        result = 1
    elif num == "2" or num == "two":
        result = 2
    elif num == "3" or num == "three":
        result = 3
    elif num == "4" or num == "four":
        result = 4
    elif num == "5" or num == "five":
        result = 5
    elif num == "6" or num == "six":
        result = 6
    elif num == "7" or num == "seven":
        result = 7
    elif num == "8" or num == "eight":
        result = 8
    elif num == "9" or num == "nine":
        result = 9
    else:
        result = 0
    return str(result)

def main():
    task2()       

if __name__ == "__main__":
    main()