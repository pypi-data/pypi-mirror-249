from typing import TYPE_CHECKING
import os

import pytest

import cq.main


if TYPE_CHECKING:
	# This is importable only when it is run through pytest
	import click.testing.CliRunner  # noqa # pylint: disable=import-error


@pytest.fixture
def cli_runner() -> 'click.testing.CliRunner':
	from click.testing import CliRunner

	return CliRunner()


def test_default_modules(cli_runner: 'click.testing.CliRunner') -> None:
	'''
	Cannot use tmpdir fixture - we need to mock cwd
	'''
	with cli_runner.isolated_filesystem():
		with open('test.py', 'w', encoding = 'utf-8') as f:
			f.write('myVar = True\n')

		result = cli_runner.invoke(cq.main.main, [])
		assert result.exit_code == 0
		assert result.output == '✓\n'


def test_result_output(cli_runner: 'click.testing.CliRunner') -> None:
	with cli_runner.isolated_filesystem():
		with open('test.py', 'w', encoding = 'utf-8') as f:
			f.write('')

		result = cli_runner.invoke(cq.main.main, [os.path.abspath(f.name)])
		assert result.exit_code == 0
		assert result.output == '✓\n'
