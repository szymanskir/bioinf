#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bioinf` package."""

import pytest

from bioinf.converters import PathToAlignmentConverter
from bioinf.path import Direction
from bioinf.sequence import Sequence
from bioinf.sequence_alignment import (
    TooLongSequenceError,
    ISequenceAlignmentAlgorithm,
    SequenceAlignmentAlgorithmConfig,
    NeedlemanWunschSequenceAlignmentAlgorithm,
    SequenceAlignmentResult,
)


def test_needleman_wunsch_alignment_score():
    config: SequenceAlignmentAlgorithmConfig = SequenceAlignmentAlgorithmConfig(
        match=5, mismatch=-5, gap=-2, max_seq_len=10, max_number_path=5
    )
    algorithm: ISequenceAlignmentAlgorithm = NeedlemanWunschSequenceAlignmentAlgorithm(
        config=config
    )
    result: SequenceAlignmentResult = algorithm.align(
        left_sequence=Sequence("MARS"), right_sequence=Sequence("SMART")
    )
    assert len(result.alignments) == 2
    assert result.score == 9


def test_needleman_wunsch_too_long_sequence_handling():
    config: SequenceAlignmentAlgorithmConfig = SequenceAlignmentAlgorithmConfig(
        match=5, mismatch=-5, gap=-2, max_seq_len=2, max_number_path=5
    )
    algorithm: ISequenceAlignmentAlgorithm = NeedlemanWunschSequenceAlignmentAlgorithm(
        config=config
    )

    with pytest.raises(TooLongSequenceError) as excinfo:
        algorithm.align(left_sequence=Sequence("MARS"), right_sequence=Sequence("SM"))

    assert str(excinfo.value) == "Left sequence is longer than 2"


def test_path_to_alignment_converter():
    converter = PathToAlignmentConverter()
    alignment = converter.convert(
        [Direction.LEFT, Direction.UP, Direction.DIAG, Direction.DIAG, Direction.LEFT],
        "EFG",
        "ABCD",
    )

    assert alignment.left_sequence_alignment == "-EFG-"
    assert alignment.right_sequence_alignment == "ABC-D"