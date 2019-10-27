from copy import deepcopy
from enum import Enum
from typing import Dict, List, Tuple


class Direction(Enum):
    DIAG = 0
    LEFT = 1
    UP = 2


class Path:
    def __init__(self, directions: List[Direction] = None):
        self._directions = [] if directions is None else directions.copy()

    def __iter__(self):
        return iter(self._directions)

    def append(self, direction: Direction) -> None:
        self._directions.append(direction)

    def copy(self):
        return deepcopy(self)

    def pop(self) -> Direction:
        return self._directions.pop()

    @classmethod
    def empty(cls):
        return cls([])
