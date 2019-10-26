#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bioinf` package."""

import pytest

from bioinf.sequence import (
    Direction,
    ISequenceAlignmentAlgorithm,
    NeedlemanWunschSequenceAlignmentAlgorithm,
    PathToAlignmentConverter,
    SequenceAlignmentResult,
)


def test_needleman_wunsch_alignment_score():
    algorithm: ISequenceAlignmentAlgorithm = NeedlemanWunschSequenceAlignmentAlgorithm(
        match=5, mismatch=-5, gap=-2
    )
    result: SequenceAlignmentResult = algorithm.align(
        left_sequence="MARS", right_sequence="SMART"
    )
    assert len(result.alignments) == 2
    assert result.score == 9


def test_path_to_alignment_converter():
    converter = PathToAlignmentConverter()
    alignment = converter.convert(
        [Direction.LEFT, Direction.UP, Direction.DIAG, Direction.DIAG, Direction.LEFT],
        "EFG",
        "ABCD",
    )

    assert alignment.left_sequence_alignment == "-EFG-"
    assert alignment.right_sequence_alignment == "ABC-D"

