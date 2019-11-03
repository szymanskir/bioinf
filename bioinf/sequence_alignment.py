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
    """Class representing a sequence alignment result.
    Attributes:
        score (int): Alignment score value.
        alignments (List[Alignment]): list of possible sequence alignments.
    """

    score: int
    alignments: List[Alignment]

    def __str__(self):
        score_string: str = f"Score = {self.score}"
        alignments_string = [str(alignment) for alignment in self.alignments]
        return score_string + "\nAlignments:\n" + "\n\n".join(alignments_string)


@dataclass
class SequenceAlignmentAlgorithmConfig:
    """Class representing a configuration of a Sequence Alignment Algorithm.

    Note: It should contain the following fields:
            - same (int) - score value for a sequence same
            - diff (int) - score value for a sequence diff
            - gap_penalty (int) - score value for adding a gap_penalty
            - max_seq_length (int) - maximum length of a sequence
            - max_number_paths (int) - maximum number of paths to retrieve
    """

    same: int
    diff: int
    gap_penalty: int
    max_seq_length: int
    max_number_paths: int


class ISequenceAlignmentAlgorithm(ABC):
    """Interface representing an alignment algorithm
    """

    @abstractclassmethod
    def align(
        self, left_sequence: Sequence, right_sequence: Sequence
    ) -> SequenceAlignmentResult:
        """Aligns two sequences and returns possible best alignments.

        Arguments:
            left_sequence (Sequence) - first sequence to align
            right_sequence (Sequence) - second sequence to align

        Returns:
            SequenceAlignmentResult - object containg the alignment
                                      score and possible alignments.
        """


class NeedlemanWunschSequenceAlignmentAlgorithm(ISequenceAlignmentAlgorithm):
    """Implementation of the Needleman-Wunsch Sequence alginment algorithm

    Arguments:
        _config (SequenceAlignmentAlgorithmConfig): Configuration of the
            sequence alignment algorithm.

    Raises:
        TooLongSequenceError: When one of the input sequence exceeds the
            length specified in the passed SequenceAlignmentAlgorithmConfig.
    """

    def __init__(self, config: SequenceAlignmentAlgorithmConfig):
        self._config = config

    def _validate_sequence(self, left_sequence: Sequence, right_sequence: Sequence):
        if len(left_sequence) > self._config.max_seq_length:
            raise TooLongSequenceError(
                f"Left sequence is longer than {self._config.max_seq_length}"
            )

        if len(right_sequence) > self._config.max_seq_length:
            raise TooLongSequenceError(
                f"Right sequence is longer than {self._config.max_seq_length}"
            )

    def _create_score_matrix(self, row_count: int, col_count: int) -> np.array:
        score_matrix: np.array = np.zeros((row_count, col_count))
        score_matrix[1:, 0] = [
            self._config.gap_penalty * ind for ind in range(1, row_count)
        ]
        score_matrix[0, 1:] = [
            self._config.gap_penalty * ind for ind in range(1, col_count)
        ]
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
            adjacency_list,
            (row_count - 1, col_count - 1),
            self._config.max_number_paths,
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
                    diag_weight = self._config.same
                else:
                    diag_weight = self._config.diff

                available_score = np.array(
                    [
                        score_matrix[row, col - 1] + self._config.gap_penalty,
                        score_matrix[row - 1, col - 1] + diag_weight,
                        score_matrix[row - 1, col] + self._config.gap_penalty,
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
