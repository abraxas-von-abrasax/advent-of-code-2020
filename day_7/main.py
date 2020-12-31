from __future__ import annotations
from typing import Optional, List

bags = {}


class Containment:
    number: int
    bag: Bag

    def __init__(self, containment: (int, Bag)):
        self.number = int(containment[0])
        self.bag = containment[1]

    @staticmethod
    def extract_info(info: str) -> (int, str):
        num, _, post = info.partition(' ')
        color, _, _ = post.partition(' bag')
        return num, color


class Bag:
    color: str
    contains: Optional[List[Containment]]

    def __init__(self, color: str):
        self.color = color
        self.contains = None


with open('input.txt') as f:
    content = [line.strip() for line in f.readlines()]


def parse_input() -> None:
    for line in content:
        col_outer, _, post = line.partition(' bags contain ')

        global bags

        if col_outer in bags:
            bag = bags[col_outer]
        else:
            bag = Bag(col_outer)
            bags[col_outer] = bag

        if post == 'no other bags.':
            continue

        other_bags = []
        buf = list(map(lambda s: s.strip(), post.split(',')))
        other_bags = list(
            map(lambda s: s[:-1] if s.endswith('.') else s, buf))
        other_bags = [Containment.extract_info(bag) for bag in other_bags]

        for other_bag in other_bags:
            num_inner = other_bag[0]
            col_inner = other_bag[1]

            if col_inner in bags:
                inner = bags[col_inner]
            else:
                inner = Bag(col_inner)
                bags[col_inner] = inner

            containment = Containment((num_inner, inner))

            if not bag.contains:
                bag.contains = []

            bag.contains.append(containment)


def search_bag(bag: Bag) -> bool:
    if bag.color == 'shiny gold':
        return True
    if not bag.contains:
        return False
    for c in bag.contains:
        inner = c.bag
        if search_bag(inner):
            return True
    return False


def count_bags(bag: Bag) -> int:
    if not bag.contains:
        return 0
    count = 0
    for c in bag.contains:
        count += (c.number + c.number * count_bags(c.bag))
    return count


def solve_first_part() -> int:
    distinct_colors = set()
    for color, bag in bags.items():
        if not bag.contains:
            continue

        found = False

        for c in bag.contains:
            found = search_bag(c.bag)
            if found:
                distinct_colors.add(color)
    return len(distinct_colors)


def solve_second_part() -> int:
    return count_bags(bags['shiny gold'])


parse_input()
print('Solution first part:', solve_first_part())
print('Solution second part:', solve_second_part())
