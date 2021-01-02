from typing import List, Dict

content: List[int] = []
cache: Dict[int, int] = {}


def parse_input() -> None:
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        global content
        content = sorted([int(line) for line in lines])
        content.append(max(content) + 3)


def solve_first_part() -> int:
    one_jolt = 0
    three_jolts = 0
    current = 0
    for jolts in content:
        diff = jolts - current
        if diff == 1:
            one_jolt += 1
        elif diff == 3:
            three_jolts += 1
        current = jolts
    return one_jolt * three_jolts


def iterate(current: int) -> int:
    global cache
    if current in cache:
        return cache[current]
    combinations = 0
    if current == max(content):
        return 1
    candidates: List[int] = []
    for jolts in content:
        if current > jolts or current == jolts:
            continue
        if (jolts - current) <= 3:
            candidates.append(jolts)
        else:
            break
    for candidate in candidates:
        combinations += iterate(candidate)
    cache[current] = combinations
    return combinations


def solve_second_part() -> int:
    global content
    total = iterate(0)
    return total


parse_input()
print('Solution first part:', solve_first_part())
print('Solution second part:', solve_second_part())
