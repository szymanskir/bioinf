# -*- coding: utf-8 -*-

"""Console script for bioinf."""
import sys
import click
from .sequence import Sequence
from .sequence_alignment import (
    NeedlemanWunschSequenceAlignmentAlgorithm,
    TooLongSequenceError,
)
from .utils import read_config, read_sequence, MissingConfigFieldError


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
    try:
        config = read_config(c)
        algorithm = NeedlemanWunschSequenceAlignmentAlgorithm(config)
        result = algorithm.align(left_sequence, right_sequence)
        click.echo(result)
    except MissingConfigFieldError as e:
        click.echo(str(e))
    except TooLongSequenceError:
        click.echo(f"One of the input sequences is longer than {config.max_seq_len}.")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
