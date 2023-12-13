import os
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    patterns = load_patterns()
    result = 0
    for pattern in patterns:
        pattern = pattern.splitlines()
        mirrors = get_possible_mirrors(pattern)
        mirror = check_possible_mirrors(pattern, mirrors)
        result += mirror
    return result


def task2():
    patterns = load_patterns()
    result = 0
    for pattern in patterns:
        pattern = pattern.splitlines()
        mirrors = [[i for i in range(1, len(pattern))], [j for j in range(1, len(pattern[0]))]]
        mirror = check_possible_mirrors_smudge(pattern, mirrors)
        result += mirror
    return result

def load_patterns():
    with open(input_file) as input:
        return re.findall(r"(?:[.#]+\n)+", input.read())

def get_possible_mirrors(pattern):
    mirrors = [[], []]
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i+1]:
            mirrors[0].append(i+1)
    for i in range(len(pattern[0]) - 1):
        if all(pattern[j][i] == pattern[j][i+1] for j in range(len(pattern))):
            mirrors[1].append(i+1)
    return mirrors

def check_possible_mirrors(pattern, mirrors):
    for m in mirrors[0]:
        smaller_side = min(m, len(pattern) - m)
        for i in range(smaller_side):
            if not pattern[m - i - 1] == pattern[m + i]:
               break
        else:
            return m * 100

    for m in mirrors[1]:
        smaller_side = min(m, len(pattern[0]) - m)
        for i in range(smaller_side):
            if not all(pattern[j][m - i - 1] == pattern[j][m + i] for j in range(len(pattern))):
               break
        else:
            return m

def check_possible_mirrors_smudge(pattern, mirrors):
    for m in mirrors[0]:
        smaller_side = min(m, len(pattern) - m)
        smudge_available = True
        for i in range(smaller_side):
            if not pattern[m - i - 1] == pattern[m + i]:
                if diff_letters(pattern[m - i - 1], pattern[m + i]) == 1 and smudge_available:
                    smudge_available = False
                else:
                    break
        else:
            if not smudge_available:
                return m * 100

    for m in mirrors[1]:
        smaller_side = min(m, len(pattern[0]) - m)
        smudge_available = True
        for i in range(smaller_side):
            if not all(pattern[j][m - i - 1] == pattern[j][m + i] for j in range(len(pattern))):
                if diff_letters("".join(pattern[j][m - i - 1] for j in range(len(pattern))), "".join(pattern[j][m + i] for j in range(len(pattern)))) == 1 and smudge_available:
                    smudge_available = False
                else:
                    break
        else:
            if not smudge_available:
                return m

def diff_letters(a,b):
    return sum(a[i] != b[i] for i in range(len(a)))

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()