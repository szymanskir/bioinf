from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from .alignment import Alignment
from .converters import PathToAlignmentConverter
from .path import Direction, Path, PathFinder
from .sequence import Sequence


class TooLongSequenceError(Exception):
    pass


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
    def align(
        self, left_sequence: Sequence, right_sequence: Sequence
    ) -> SequenceAlignmentResult:
        pass


class NeedlemanWunschSequenceAlignmentAlgorithm(ISequenceAlignmentAlgorithm):
    def __init__(self, config: SequenceAlignmentAlgorithmConfig):
        self._config = config

    def _validate_sequence(self, left_sequence: Sequence, right_sequence: Sequence):
        if len(left_sequence) > self._config.max_seq_len:
            raise TooLongSequenceError(
                f"Left sequence is longer than {self._config.max_seq_len}"
            )

        if len(right_sequence) > self._config.max_seq_len:
            raise TooLongSequenceError(
                f"Right sequence is longer than {self._config.max_seq_len}"
            )

    def _create_score_matrix(self, row_count: int, col_count: int) -> np.array:
        score_matrix: np.array = np.zeros((row_count, col_count))
        score_matrix[1:, 0] = [self._config.gap * ind for ind in range(1, row_count)]
        score_matrix[0, 1:] = [self._config.gap * ind for ind in range(1, col_count)]
        return score_matrix

    def _create_adjacency_list(
        self, row_count: int, col_count: int
    ) -> Dict[Tuple[int, int], List[Direction]]:
        adjacency_list: Dict[Tuple[int, int], List[Direction]] = dict()

        for row in range(1, row_count):
            adjacency_list[(row, 0)] = [Direction.UP]

        for col in range(1, col_count):
            adjacency_list[(0, col)] = [Direction.LEFT]

        return adjacency_list

    def _retrieve_paths(self, adjacency_list, row_count, col_count):
        path_finder: PathFinder = PathFinder(
            adjacency_list, (row_count - 1, col_count - 1), self._config.max_number_path
        )
        paths: List[Path] = path_finder.find_all_paths()

        return paths

    def align(
        self, left_sequence: Sequence, right_sequence: Sequence
    ) -> SequenceAlignmentResult:
        self._validate_sequence(
            left_sequence=left_sequence, right_sequence=right_sequence
        )
        row_count: int = len(left_sequence) + 1
        col_count: int = len(right_sequence) + 1
        score_matrix: np.array = self._create_score_matrix(row_count, col_count)
        adjacency_list = self._create_adjacency_list(row_count, col_count)

        for row in range(1, row_count):
            for col in range(1, col_count):
                if left_sequence[row - 1] == right_sequence[col - 1]:
                    diag_weight = self._config.match
                else:
                    diag_weight = self._config.mismatch

                available_score = np.array(
                    [
                        score_matrix[row, col - 1] + self._config.gap,
                        score_matrix[row - 1, col - 1] + diag_weight,
                        score_matrix[row - 1, col] + self._config.gap,
                    ]
                )

                available_paths = np.array(
                    [Direction.LEFT, Direction.DIAG, Direction.UP]
                )

                current_score = np.max(available_score)
                current_paths = available_paths[available_score == current_score]

                score_matrix[row, col] = current_score
                adjacency_list[(row, col)] = current_paths.tolist()

        score: int = score_matrix[row_count - 1, col_count - 1]
        paths = self._retrieve_paths(adjacency_list, row_count, col_count)
        alignments: List[Alignment] = [
            PathToAlignmentConverter.convert(path, left_sequence, right_sequence)
            for path in paths
        ]
        return SequenceAlignmentResult(score, alignments)