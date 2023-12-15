import os
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    strings = load_strings()

    return sum(calculate_hash_value(string) for string in strings)

def task2():
    strings = load_strings()

    boxes = [[] for i in range(256)]

    for string in strings:
        label, label_hash, operation, focal_length = parse_lens_string(string)
        box = boxes[label_hash]
        if operation:
            for i in range(len(box)):
                if box[i][0] == label:
                    box[i][1] = focal_length
                    break
            else:
                box.append([label, focal_length])
        else:
            for lens in box:
                if lens[0] == label:
                    box.remove(lens)
                    break
    
    result = 0
    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            result += (i + 1) * (j + 1) * boxes[i][j][1]
    
    return result   

def load_strings():
    with open(input_file) as input:
        return re.findall(r"[^,\n]+", input.read())

def calculate_hash_value(string):
    hash_value = 0
    for c in string:
        hash_value += ord(c)
        hash_value *= 17
        hash_value %= 256
    return hash_value

def parse_lens_string(string):
    label = re.findall(r"[a-z]+", string)[0]
    label_hash = calculate_hash_value(label)
    operation = "=" in string
    if operation:
        focal_length = int(string[-1])
    else:
        focal_length = 0
    return (label, label_hash, operation, focal_length)

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()