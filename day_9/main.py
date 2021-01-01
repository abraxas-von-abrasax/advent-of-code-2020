content = []


def parse_input() -> None:
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        global content
        content = [int(line) for line in lines]


def solve_first_part() -> int:
    global content
    chunk_size = 25
    shift = 0
    while True:
        target_index = chunk_size + shift
        test_num = content[target_index]
        start = target_index - chunk_size
        test_arr = content[start:target_index]
        found_pair = False
        for i, a in enumerate(test_arr):
            for j, b in enumerate(test_arr):
                if i == j:
                    continue
                if a + b == test_num:
                    found_pair = True
                    break
            if found_pair:
                break

        if not found_pair:
            return test_num

        shift += 1


def solve_second_part() -> int:
    global content
    invalid_num = solve_first_part()
    start = 0
    while True:
        current = start + 1
        buf = content[start]
        overflow = False

        while current < len(content):
            buf += content[current]
            if buf > invalid_num:
                overflow = True
                break
            elif buf == invalid_num:
                break
            current += 1
        else:
            overflow = True

        if not overflow:
            target_arr = content[start:current + 1]
            return min(target_arr) + max(target_arr)
        start += 1


parse_input()
print('Solution first part:', solve_first_part())
print('Solution second part:', solve_second_part())
