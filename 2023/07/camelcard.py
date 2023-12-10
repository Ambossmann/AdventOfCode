import re
import os
from collections import Counter

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_file = os.path.join(__location__, "input.txt")

def task1():
    result = 0
    with open(input_file) as input:
        parsed_input = []
        for line in input:
            hand, bid = line.rstrip().split(" ")
            parsed_input.append((hand_value1(hand), int(bid)))
        parsed_input.sort()
        for i in range(len(parsed_input)):
            winnings = parsed_input[i][1] * (i + 1)
            result += winnings
    return result


def task2():
    result = 0
    with open(input_file) as input:
        parsed_input = []
        for line in input:
            hand, bid = line.rstrip().split(" ")
            parsed_input.append((hand_value2(hand), int(bid)))
        parsed_input.sort()
        for i in range(len(parsed_input)):
            winnings = parsed_input[i][1] * (i + 1)
            result += winnings
    return result

def hand_value1(hand):
    mcc = Counter(hand).most_common(2)
    hand_type = 0
    if mcc[0][1] >= 4:
        hand_type = mcc[0][1] + 1
    elif mcc[0][1] == 3:
        if mcc[1][1] == 2:
            hand_type = 4
        else:
            hand_type = 3
    elif mcc[0][1] == 2:
        if mcc[1][1] == 2:
            hand_type = 2
        else:
            hand_type = 1
    else:
        hand_type = 0
    hand_value = card_value1(hand[0]) << 16
    hand_value |= card_value1(hand[1]) << 12
    hand_value |= card_value1(hand[2]) << 8
    hand_value |= card_value1(hand[3]) << 4
    hand_value |= card_value1(hand[4])
    return (hand_type, hand_value)

def card_value1(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    elif card == "T":
        return 10
    else:
        return int(card)

def hand_value2(hand):
    mcc = Counter(hand).most_common()
    joker_count = hand.count("J")
    hand_type = 0
    if mcc[0][1] < 5:
        if mcc[0][0] == "J":
            mcc.pop(0)
        mcc[0] = (mcc[0][0], mcc[0][1] + joker_count)
    
    if mcc[0][1] >= 4:
        hand_type = mcc[0][1] + 1
    elif mcc[0][1] == 3:
        if mcc[1][1] == 2:
            hand_type = 4
        else:
            hand_type = 3
    elif mcc[0][1] == 2:
        if mcc[1][1] == 2:
            hand_type = 2
        else:
            hand_type = 1
    else:
        hand_type = 0
    hand_value = card_value2(hand[0]) << 16
    hand_value |= card_value2(hand[1]) << 12
    hand_value |= card_value2(hand[2]) << 8
    hand_value |= card_value2(hand[3]) << 4
    hand_value |= card_value2(hand[4])
    return (hand_type, hand_value)

def card_value2(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 1
    elif card == "T":
        return 10
    else:
        return int(card)

def main():
    print(task1())
    print(task2())

if __name__ == "__main__":
    main()