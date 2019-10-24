from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Alignment:
    left_sequence_alignment: str
    right_sequence_alignment: str


@dataclass
class SequenceAlignmentResult:
    score: int
    alignments: List[Alignment]


@dataclass
class SequenceAlignmentAlgorithmConfig:
    match: int
    mismatch: int
    gap: int


class ISequenceAlignmentAlgorithm(ABC):
    @abstractclassmethod
    def align(self, left_sequence: str, right_sequence: str) -> SequenceAlignmentResult:
        pass


class NeedlemanWunschSequenceAlignmentAlgorithm(ISequenceAlignmentAlgorithm):
    def __init__(self, match: int, mismatch: int, gap: int):
        self._match: int = match
        self._mismatch: int = mismatch
        self._gap: int = gap

    def _create_score_matrix(self, row_count: int, col_count: int) -> np.array:
        score_matrix: np.array = np.zeros((row_count, col_count))
        score_matrix[1:, 0] = [self._gap * ind for ind in range(1, row_count)]
        score_matrix[0, 1:] = [self._gap * ind for ind in range(1, col_count)]
        return score_matrix

    def align(self, left_sequence: str, right_sequence: str) -> SequenceAlignmentResult:
        row_count = len(left_sequence) + 1
        col_count = len(right_sequence) + 1
        score_matrix: np.array = self._create_score_matrix(row_count, col_count)

        for row in range(1, row_count):
            for col in range(1, col_count):
                diag_weight: int = self._match if left_sequence[
                    row - 1
                ] == right_sequence[col - 1] else self._mismatch
                score_matrix[row, col] = max(
                    score_matrix[row, col - 1] + self._gap,
                    score_matrix[row - 1, col - 1] + diag_weight,
                    score_matrix[row - 1, col] + self._gap,
                )

        score: int = score_matrix[row_count - 1, col_count - 1]

        return SequenceAlignmentResult(score, [])

    @classmethod
    def from_config(cls, config: SequenceAlignmentAlgorithmConfig):
        return cls(match=config.match, mismatch=config.mismatch, gap=config.gap)
