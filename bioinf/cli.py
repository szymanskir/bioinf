# -*- coding: utf-8 -*-

"""Console script for bioinf."""
import sys
import click
from .sequence import Sequence
from .sequence_alignment import (
    NeedlemanWunschSequenceAlignmentAlgorithm,
    TooLongSequenceError,
)
from .utils import read_config, read_sequence


@click.group()
def main(args=None):
    """Console script for bioinf."""
    return 0


@main.command()
@click.option("-a", type=click.Path(exists=True))
@click.option("-b", type=click.Path(exists=True))
@click.option("-c", type=click.Path(exists=True))
def align(a: str, b: str, c: str):
    left_sequence: Sequence = read_sequence(a)
    right_sequence: Sequence = read_sequence(b)
    config = read_config(c)
    algorithm = NeedlemanWunschSequenceAlignmentAlgorithm(config)
    try:
        result = algorithm.align(left_sequence, right_sequence)
        click.echo(result)
    except TooLongSequenceError as e:
        click.echo(f"One of the input sequences is longer than {config.max_seq_len}.")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
