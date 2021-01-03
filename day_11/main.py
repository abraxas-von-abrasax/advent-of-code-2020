from __future__ import annotations, with_statement
from enum import Enum
from typing import Optional, List


class LocationState(Enum):
    FREE = 'free',
    OCCUPIED = 'occupied',
    FLOOR = 'floor'


class Location:
    current_state: LocationState
    new_state: Optional[LocationState]

    def __init__(self, field: str):
        if field == 'L':
            self.current_state = LocationState.FREE
        else:
            self.current_state = LocationState.FLOOR
        self.new_state = None

    def get_state(self) -> LocationState:
        return self.current_state

    def transform(self) -> None:
        if not self.new_state:
            return
        self.current_state = self.new_state
        self.new_state = None

    def set_occupied(self) -> None:
        self.new_state = LocationState.OCCUPIED

    def set_free(self) -> None:
        self.new_state = LocationState.FREE

    def is_floor(self) -> bool:
        return self.current_state == LocationState.FLOOR

    def is_occupied(self) -> bool:
        return self.current_state == LocationState.OCCUPIED


class Model:
    field: List[Location] = []
    width: int

    def __init__(self, field: List[Location], width: int):
        self.field = field
        self.width = width

    def do_round(self) -> bool:
        has_changed = False
        x = 0
        y = 0
        for i in range(0, len(self.field)):
            x = i % self.width
            if i != 0 and i % self.width == 0:
                y += 1
            if self.check(x, y):
                has_changed = True
        for loc in self.field:
            loc.transform()
        return has_changed

    def check(self, x: int, y: int) -> bool:
        index = x + y * self.width
        if index >= len(self.field):
            return False
        this = self.field[index]
        if this.is_floor():
            return False
        if not this.is_occupied() and self.__should_occupy(x, y):
            this.set_occupied()
            return True
        elif this.is_occupied() and self.__should_free(x, y):
            this.set_free()
            return True

    def num_occupied(self) -> int:
        return len(list(filter(lambda loc: loc.is_occupied(), self.field)))

    def __should_occupy(self, x: int, y: int) -> bool:
        surrounding_fields = self.__get_surrounding_fields(x, y)
        for field in surrounding_fields:
            if field.is_floor():
                continue
            elif field.is_occupied():
                return False
        return True

    def __should_free(self, x: int, y: int) -> bool:
        surrounding_fields = self.__get_surrounding_fields(x, y)
        occupied_count = 0
        for field in surrounding_fields:
            if field.is_floor():
                continue
            elif field.is_occupied():
                occupied_count += 1
        return occupied_count >= 4

    def __get_state(self, x: int, y: int) -> LocationState:
        index = x + y * self.width
        return self.field[index].get_state()

    def __get_surrounding_fields(self, x: int, y: int) -> List[Location]:
        res = []
        if self.__top_left(x, y):
            res.append(self.__top_left(x, y))
        if self.__top_center(x, y):
            res.append(self.__top_center(x, y))
        if self.__top_right(x, y):
            res.append(self.__top_right(x, y))
        if self.__center_left(x, y):
            res.append(self.__center_left(x, y))
        if self.__center_right(x, y):
            res.append(self.__center_right(x, y))
        if self.__bottom_left(x, y):
            res.append(self.__bottom_left(x, y))
        if self.__bottom_center(x, y):
            res.append(self.__bottom_center(x, y))
        if self.__bottom_right(x, y):
            res.append(self.__bottom_right(x, y))
        return res

    def __top_left(self, x: int, y: int) -> Optional[Location]:
        if x == 0 or (y == 0 and 0 <= x < self.width):
            return None
        coord = (x - 1) + (y - 1) * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __top_center(self, x: int, y: int) -> Optional[Location]:
        if y == 0:
            return None
        coord = x + (y - 1) * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __top_right(self, x: int, y: int) -> Optional[Location]:
        if x == self.width - 1 or (y == 0 and 0 <= x < self.width):
            return None
        coord = (x + 1) + (y - 1) * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __center_left(self, x: int, y: int) -> Optional[Location]:
        if x == 0:
            return None
        coord = (x - 1) + y * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __center_right(self, x: int, y: int) -> Optional[Location]:
        if x == self.width - 1:
            return None
        coord = (x + 1) + y * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __bottom_left(self, x: int, y: int) -> Optional[Location]:
        if x == 0 or (y == len(self.field) - 1 and 0 <= x < self.width):
            return None
        coord = (x - 1) + (y + 1) * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __bottom_center(self, x: int, y: int) -> Optional[Location]:
        if y == len(self.field) - 1:
            return None
        coord = x + (y + 1) * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]

    def __bottom_right(self, x: int, y: int) -> Optional[Location]:
        if x == self.width - 1 or (y == len(self.field) - 1 and 0 <= x < self.width):
            return None
        coord = (x + 1) + (y + 1) * self.width
        if coord >= len(self.field) or coord < 0:
            return None
        return self.field[coord]


def parse_input() -> Model:
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        width = len(lines[0])
        field: List[Location] = []
        for line in lines:
            for char in line:
                field.append(Location(char))
        return Model(field, width)


def solve_first_part(model: Model) -> int:
    while model.do_round():
        pass
    return model.num_occupied()


model = parse_input()
print('Solution first part:', solve_first_part(model))
