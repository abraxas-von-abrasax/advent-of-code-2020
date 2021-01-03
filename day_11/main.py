from __future__ import annotations, with_statement
from enum import Enum
from typing import Optional, List, NewType


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

    def print(self) -> None:
        if self.current_state == LocationState.FLOOR:
            print('.', end='')
        elif self.current_state == LocationState.FREE:
            print('L', end='')
        else:
            print('#', end='')


Row = NewType('Row', List[Location])


class Model:
    field: List[Row]
    width: int

    def __init__(self, field: List[Location], width: int, height: int):
        self.field = field
        self.width = width
        self.height = height

    def do_round(self, min_occupied: int, only_check_immediate: bool) -> bool:
        has_changed = False
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.check(row, col, min_occupied, only_check_immediate):
                    has_changed = True
        for row in self.field:
            for loc in row:
                loc.transform()
        return has_changed

    def check(self, row: int, col: int, min_occupied: int,
              only_check_immediate: bool) -> bool:
        if not self.__check_coordinates(row, col):
            return False
        this = self.field[row][col]
        if this.is_floor():
            return False
        if not this.is_occupied() and self.__should_occupy(
                row, col, only_check_immediate):
            this.set_occupied()
            return True
        elif this.is_occupied() and self.__should_free(row, col, min_occupied, only_check_immediate):
            this.set_free()
            return True

    def num_occupied(self) -> int:
        occupied = 0
        for row in self.field:
            for el in row:
                if el.is_occupied():
                    occupied += 1
        return occupied

    def __should_occupy(self, row: int, col: int,
                        only_check_immediate: bool) -> bool:
        surrounding_fields = self.__get_surrounding_fields(
            row, col, only_check_immediate)
        for field in surrounding_fields:
            if field.is_floor():
                continue
            elif field.is_occupied():
                return False
        return True

    def __should_free(
        self, row: int, col: int, min_occupied: int,
            only_check_immediate: bool) -> bool:
        surrounding_fields = self.__get_surrounding_fields(
            row, col, only_check_immediate)
        occupied_count = 0
        for field in surrounding_fields:
            if field.is_floor():
                continue
            elif field.is_occupied():
                occupied_count += 1
        return occupied_count >= min_occupied

    def __get_surrounding_fields(
            self, row: int, col: int, only_check_immediate: bool) -> List[Location]:
        res = []
        top_left = self.__top_left(row, col, only_check_immediate)
        if top_left:
            res.append(top_left)
        top_center = self.__top_center(row, col, only_check_immediate)
        if top_center:
            res.append(top_center)
        top_right = self.__top_right(row, col, only_check_immediate)
        if top_right:
            res.append(top_right)
        center_left = self.__center_left(row, col, only_check_immediate)
        if center_left:
            res.append(center_left)
        center_right = self.__center_right(row, col, only_check_immediate)
        if center_right:
            res.append(center_right)
        bottom_left = self.__bottom_left(row, col, only_check_immediate)
        if bottom_left:
            res.append(bottom_left)
        bottom_center = self.__bottom_center(row, col, only_check_immediate)
        if bottom_center:
            res.append(bottom_center)
        bottom_right = self.__bottom_right(row, col, only_check_immediate)
        if bottom_right:
            res.append(bottom_right)
        return res

    def __check_coordinates(self, row: int, col: int) -> bool:
        return (0 <= row < self.height) and (0 <= col < self.width)

    def __top_left(self, row: int, col: int,
                   only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row - diff
            dCol = col - diff
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __top_center(self, row: int, col: int,
                     only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row - diff
            dCol = col
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __top_right(self, row: int, col: int,
                    only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row - diff
            dCol = col + diff
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __center_left(self, row: int, col: int,
                      only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row
            dCol = col - diff
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __center_right(self, row: int, col: int,
                       only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row
            dCol = col + diff
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __bottom_left(self, row: int, col: int,
                      only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row + diff
            dCol = col - diff
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __bottom_center(self, row: int, col: int,
                        only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row + diff
            dCol = col
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def __bottom_right(self, row: int, col: int,
                       only_check_immediate: bool) -> Optional[Location]:
        diff = 1
        while True:
            dRow = row + diff
            dCol = col + diff
            if not self.__check_coordinates(dRow, dCol):
                return None
            if only_check_immediate:
                return self.field[dRow][dCol]
            elif not self.field[dRow][dCol].is_floor():
                return self.field[dRow][dCol]
            diff += 1

    def print(self) -> None:
        for row in self.field:
            for el in row:
                el.print()
            print('')


def parse_input() -> Model:
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        width = len(lines[0])
        height = len(lines)
        field: List[Row] = []
        for line in lines:
            row: Row = []
            for char in line:
                row.append(Location(char))
            field.append(row)
        return Model(field, width, height)


def solve_first_part(model: Model) -> int:
    while model.do_round(4, True):
        pass
    return model.num_occupied()


def solve_second_part(model: Model) -> int:
    while model.do_round(5, False):
        pass
    return model.num_occupied()


model = parse_input()
print('Solution first part:', solve_first_part(model))
model = parse_input()
print('Solution second part:', solve_second_part(model))
