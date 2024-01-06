#!/usr/bin/env python

"""Tests for `pickle_data_file_utils` package."""


import unittest
from click.testing import CliRunner

from pickle_data_file_utils import pickle_data_file_utils
from pickle_data_file_utils import cli


class TestPickle_data_file_utils(unittest.TestCase):
    """Tests for `pickle_data_file_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'pickle_data_file_utils.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
