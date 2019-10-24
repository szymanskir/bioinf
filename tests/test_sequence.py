#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bioinf` package."""

import pytest

from bioinf.sequence import (
    ISequenceAlignmentAlgorithm,
    NeedlemanWunschSequenceAlignmentAlgorithm,
    SequenceAlignmentResult,
)


def test_needleman_wunsch_alignment_score():
    algorithm: ISequenceAlignmentAlgorithm = NeedlemanWunschSequenceAlignmentAlgorithm(
        match=5, mismatch=-5, gap=-2
    )
    result: SequenceAlignmentResult = algorithm.align(
        left_sequence="GAAC", right_sequence="CAAGAC"
    )
    assert result.score == 7
