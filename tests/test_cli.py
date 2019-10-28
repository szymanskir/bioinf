#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bioinf` package."""

import pytest

from click.testing import CliRunner

from bioinf import cli


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_cli_too_long_input_error_handling():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align, ["-a", "along.txt", "-b", "b.txt", "-c", "config.ini"]
    )
    assert help_result.exit_code == 0
    assert "One of the input sequences is longer than" in help_result.output


def test_cli_too_wrong_config_error_handling():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(
        cli.align, ["-a", "a.txt", "-b", "b.txt", "-c", "config_missing.ini"]
    )
    assert help_result.exit_code == 0
    assert "is missing from the config file" in help_result.output
