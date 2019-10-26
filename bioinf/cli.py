# -*- coding: utf-8 -*-

"""Console script for bioinf."""
import sys
import click
from .sequence import NeedlemanWunschSequenceAlignmentAlgorithm
from .utils import read_config, read_sequence


@click.group()
def main(args=None):
    """Console script for bioinf."""
    click.echo("Replace this message by putting your code into " "bioinf.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


@main.command()
@click.option("-a", type=click.Path(exists=True))
@click.option("-b", type=click.Path(exists=True))
@click.option("-c", type=click.Path(exists=True))
def align(a: str, b: str, c: str):
    left_sequence: str = read_sequence(a)
    right_sequence: str = read_sequence(b)
    config = read_config(c)
    algorithm = NeedlemanWunschSequenceAlignmentAlgorithm.from_config(config)
    result = algorithm.align(left_sequence, right_sequence)
    click.echo(result)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
