from typing import List, Tuple, NewType
from copy import deepcopy

Instrution = NewType('Instruction', Tuple[str, int, bool])
content: List[Instrution] = []


def get_content() -> List[Instrution]:
    return deepcopy(content)


def parse_input() -> None:
    global content
    with open('input.txt') as f:
        content = [line.strip() for line in f.readlines()]
        content = [line.partition(' ') for line in content]
        content = [
            {'op': tup[0],
             'val': int(tup[2]),
             'visited': False} for tup in content]


def solve_first_part() -> int:
    c = get_content()
    acc = 0
    i = 0
    while True:
        instruction = c[i]
        if instruction['visited'] == True:
            break
        instruction['visited'] = True
        if instruction['op'] == 'jmp':
            i += instruction['val']
            continue
        elif instruction['op'] == 'acc':
            acc += instruction['val']
        i += 1
    return acc


def solve_second_part() -> int:
    next_to_modify = 0

    while True:
        c = get_content()
        acc = 0
        i = 0
        while i < len(content):

            instruction = c[i]
            if instruction['visited'] == True:
                break
            instruction['visited'] = True

            if next_to_modify == i:
                if instruction['op'] == 'jmp':
                    instruction['op'] = 'nop'
                elif instruction['op'] == 'nop':
                    instruction['op'] = 'jmp'
                else:
                    break

            if instruction['op'] == 'jmp':
                i += instruction['val']
                continue
            elif instruction['op'] == 'acc':
                acc += instruction['val']
            i += 1
        else:
            return acc

        next_to_modify += 1


parse_input()
print('Solution first part:', solve_first_part())
print('Solution second part:', solve_second_part())
