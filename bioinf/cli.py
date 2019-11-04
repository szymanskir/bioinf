# -*- coding: utf-8 -*-

"""Console script for bioinf."""
import sys
import click
from .sequence import Sequence
from .sequence_alignment import NeedlemanWunschSequenceAlignmentAlgorithm
from .utils import read_config, read_sequence


@click.group()
def main(args=None):
    """Console script for bioinf."""


@main.command()
@click.option("-a", type=click.Path(exists=True), required=True)
@click.option("-b", type=click.Path(exists=True), required=True)
@click.option("-c", type=click.Path(exists=True), required=True)
@click.option("-o", type=click.Path())
def align(a: str, b: str, c: str, o: str):
    try:
        left_sequence: Sequence = read_sequence(a)
        right_sequence: Sequence = read_sequence(b)
        config = read_config(c)
        algorithm = NeedlemanWunschSequenceAlignmentAlgorithm(config)
        result = algorithm.align(left_sequence, right_sequence)
        if o:
            with open(o, "w") as f:
                f.write(str(result))
        else:
            click.echo(result)
    except Exception as e:
        click.echo(str(e))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
