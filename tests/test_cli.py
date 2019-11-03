#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bioinf` package."""

import pytest

from click.testing import CliRunner

from bioinf import cli
from os.path import dirname, join


def get_relative_path(filepath: str):
    return join(dirname(__file__), filepath)


@pytest.fixture
def a_sequence_filepath():
    return get_relative_path("resources/a.txt")


@pytest.fixture
def b_sequence_filepath():
    return get_relative_path("resources/b.txt")


@pytest.fixture
def along_sequence_filepath():
    return get_relative_path("resources/along.txt")


@pytest.fixture
def config_filepath():
    return get_relative_path("resources/config.ini")


@pytest.fixture
def config_missing_field_filepath():
    return get_relative_path("resources/config_missing_field.ini")


@pytest.fixture
def wrong_fasta_no_description():
    return get_relative_path("resources/wrong_fasta-no_description.txt")


def test_cli_no_output_file(a_sequence_filepath, b_sequence_filepath, config_filepath):
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align,
        ["-a", a_sequence_filepath, "-b", b_sequence_filepath, "-c", config_filepath],
    )
    assert help_result.exit_code == 0
    assert "Score = 9" in help_result.output


def test_cli_output_file(
    a_sequence_filepath, b_sequence_filepath, config_filepath, tmp_path
):
    tmp_file = tmp_path / "result.txt"
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align,
        [
            "-a",
            a_sequence_filepath,
            "-b",
            b_sequence_filepath,
            "-c",
            config_filepath,
            "-o",
            tmp_file,
        ],
    )
    with open(tmp_file, "r") as f:
        result = f.read()
    assert help_result.exit_code == 0
    assert "Score = 9" in result


def test_cli_too_long_left_input_error_handling(
    along_sequence_filepath, b_sequence_filepath, config_filepath
):
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align,
        [
            "-a",
            along_sequence_filepath,
            "-b",
            b_sequence_filepath,
            "-c",
            config_filepath,
        ],
    )
    assert help_result.exit_code == 0
    assert "is longer than" in help_result.output


def test_cli_too_long_right_input_error_handling(
    along_sequence_filepath, b_sequence_filepath, config_filepath
):
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align,
        [
            "-a",
            b_sequence_filepath,
            "-b",
            along_sequence_filepath,
            "-c",
            config_filepath,
        ],
    )
    assert help_result.exit_code == 0
    assert "is longer than" in help_result.output


def test_cli_too_wrong_config_error_handling(
    a_sequence_filepath, b_sequence_filepath, config_missing_field_filepath
):
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align,
        [
            "-a",
            a_sequence_filepath,
            "-b",
            b_sequence_filepath,
            "-c",
            config_missing_field_filepath,
        ],
    )
    assert help_result.exit_code == 0
    assert "is missing from the config file" in help_result.output


def test_cli_bad_fasta_file_error_handling(
    a_sequence_filepath, wrong_fasta_no_description, config_filepath
):
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align,
        [
            "-a",
            a_sequence_filepath,
            "-b",
            wrong_fasta_no_description,
            "-c",
            config_filepath,
        ],
    )
    assert help_result.exit_code == 0
    assert "does not start with `>`" in help_result.output
