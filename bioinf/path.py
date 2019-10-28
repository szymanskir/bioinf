from copy import deepcopy
from enum import Enum
from typing import Dict, List, Tuple


class Direction(Enum):
    """Class representing possible directions
    """

    DIAG = 0
    LEFT = 1
    UP = 2


class Path:
    """Class representing a Path -- a list of directions.
    
    Attributes:
        _directions (List[Direction]): list of direction of which the
            path is composed.
    """

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


class PathFinder:
    def __init__(
        self,
        adjacency_list: Dict[Tuple[int, int], List[Direction]],
        last_cell: Tuple[int, int],
        max_number_path: int,
    ):
        self._adjacency_list: Dict[Tuple[int, int], List[Direction]] = adjacency_list
        self._last_cell: Tuple[int, int] = last_cell
        self._max_number_path: int = max_number_path
        self._stop_flag = False

    def _get_next_cell(
        self, current_cell: Tuple[int, int], direction: Direction
    ) -> Tuple[int, int]:
        mappings = {
            Direction.LEFT: (current_cell[0], current_cell[1] - 1),
            Direction.DIAG: (current_cell[0] - 1, current_cell[1] - 1),
            Direction.UP: (current_cell[0] - 1, current_cell[1]),
        }

        return mappings[direction]

    def _find_all_paths_helper(self, current_cell: Tuple[int, int]) -> None:
        if current_cell == (0, 0):
            self._paths.append(self._current_path.copy())
            if len(self._paths) >= self._max_number_path:
                self._stop_flag = True
            return

        for direction in self._adjacency_list[current_cell]:
            if self._stop_flag:
                return
            next_cell: Tuple[int, int] = self._get_next_cell(current_cell, direction)
            self._current_path.append(direction)
            self._find_all_paths_helper(next_cell)
            self._current_path.pop()

    def find_all_paths(self) -> List[Path]:
        self._paths: List[Path] = []
        self._current_path: Path = Path.empty()
        self._find_all_paths_helper(self._last_cell)

        return self._paths
