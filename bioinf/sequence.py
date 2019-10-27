from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Dict, List, Tuple

import numpy as np


class Direction(Enum):
    DIAG = 0
    LEFT = 1
    UP = 2


@dataclass
class Alignment:
    left_sequence_alignment: str
    right_sequence_alignment: str

    def __str__(self):
        return f"{self.left_sequence_alignment}\n{self.right_sequence_alignment}"


class PathFinder:
    def __init__(
        self,
        adjacency_list: Dict[Tuple[int, int], List[Direction]],
        row_count: int,
        col_count: int,
        max_number_path: int,
    ):
        self._adjacency_list: Dict[Tuple[int, int], List[Direction]] = adjacency_list
        self._row_count: int = row_count
        self._col_count: int = col_count
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

    def find_all_paths(self):
        self._paths: List[List[Direction]] = []
        self._current_path: List[Direction] = []
        self._find_all_paths_helper((self._row_count - 1, self._col_count - 1))

        return self._paths


class PathToAlignmentConverter:
    @staticmethod
    def convert(
        path: List[Direction], left_sequence: str, right_sequence: str
    ) -> Alignment:
        left_sequence_alignment = ""
        right_sequence_alignment = ""
        left_index = len(left_sequence)
        right_index = len(right_sequence)

        for direction in path:
            if direction == Direction.DIAG:
                left_index = left_index - 1
                right_index = right_index - 1
                left_sequence_alignment = (
                    left_sequence[left_index] + left_sequence_alignment
                )
                right_sequence_alignment = (
                    right_sequence[right_index] + right_sequence_alignment
                )
            if direction == Direction.UP:
                left_index = left_index - 1
                left_sequence_alignment = (
                    left_sequence[left_index] + left_sequence_alignment
                )
                right_sequence_alignment = "-" + right_sequence_alignment
            if direction == Direction.LEFT:
                right_index = right_index - 1
                left_sequence_alignment = "-" + left_sequence_alignment
                right_sequence_alignment = (
                    right_sequence[right_index] + right_sequence_alignment
                )

        return Alignment(left_sequence_alignment, right_sequence_alignment)


@dataclass
class SequenceAlignmentResult:
    score: int
    alignments: List[Alignment]

    def __str__(self):
        score_string: str = f"Score: {self.score}"
        alignments_string = [str(alignment) for alignment in self.alignments]
        return score_string + "\nAlignments:\n" + "\n\n".join(alignments_string)


@dataclass
class SequenceAlignmentAlgorithmConfig:
    match: int
    mismatch: int
    gap: int
    max_seq_len: int
    max_number_path: int


class ISequenceAlignmentAlgorithm(ABC):
    @abstractclassmethod
    def align(self, left_sequence: str, right_sequence: str) -> SequenceAlignmentResult:
        pass


class NeedlemanWunschSequenceAlignmentAlgorithm(ISequenceAlignmentAlgorithm):
    def __init__(self, config: SequenceAlignmentAlgorithmConfig):
        self._config = config

    def _create_score_matrix(self, row_count: int, col_count: int) -> np.array:
        score_matrix: np.array = np.zeros((row_count, col_count))
        score_matrix[1:, 0] = [self._config.gap * ind for ind in range(1, row_count)]
        score_matrix[0, 1:] = [self._config.gap * ind for ind in range(1, col_count)]
        return score_matrix

    def _create_adjacency_list(
        self, row_count: int, col_count: int
    ) -> Dict[Tuple[int, int], List[Direction]]:
        adjacency_list: Dict[Tuple[int, int], List[Direction]] = dict()

        for ind in product(range(row_count), range(col_count)):
            adjacency_list[ind] = []

        for row in range(1, row_count):
            adjacency_list[(row, 0)].append(Direction.UP)

        for col in range(1, col_count):
            adjacency_list[(0, col)].append(Direction.LEFT)

        return adjacency_list

    def align(self, left_sequence: str, right_sequence: str) -> SequenceAlignmentResult:
        row_count = len(left_sequence) + 1
        col_count = len(right_sequence) + 1
        score_matrix: np.array = self._create_score_matrix(row_count, col_count)
        adjacency_list = self._create_adjacency_list(row_count, col_count)

        for row in range(1, row_count):
            for col in range(1, col_count):
                if left_sequence[row - 1] == right_sequence[col - 1]:
                    diag_weight = self._config.match
                else:
                    diag_weight = self._config.mismatch

                current_score = max(
                    score_matrix[row, col - 1] + self._config.gap,
                    score_matrix[row - 1, col - 1] + diag_weight,
                    score_matrix[row - 1, col] + self._config.gap,
                )

                if current_score == score_matrix[row, col - 1] + self._config.gap:
                    adjacency_list[(row, col)].append(Direction.LEFT)
                if current_score == score_matrix[row - 1, col - 1] + diag_weight:
                    adjacency_list[(row, col)].append(Direction.DIAG)
                if current_score == score_matrix[row - 1, col] + self._config.gap:
                    adjacency_list[(row, col)].append(Direction.UP)

                score_matrix[row, col] = current_score

        score: int = score_matrix[row_count - 1, col_count - 1]
        path_finder: PathFinder = PathFinder(
            adjacency_list, row_count, col_count, self._config.max_number_path
        )
        paths: List[List[Direction]] = path_finder.find_all_paths()
        alignments: List[Alignment] = [
            PathToAlignmentConverter.convert(path, left_sequence, right_sequence)
            for path in paths
        ]

        return SequenceAlignmentResult(score, alignments)
