from typing import Any
import pathlib

import pytest

import cq.checker
import cq.checkers.orange as orange
import cq.utils


@pytest.mark.parametrize('filename', ('not-formatted.txt', 'formatted.txt'))
def test_runner_with_orange_installed(filename: str) -> None:
	checker = orange.OrangeChecker()
	test_file = pathlib.Path(__file__).parent / f'data/{filename}'
	actual_result = checker.run([str(test_file.resolve())])
	if filename == 'not-formatted.txt':
		assert actual_result.return_code == 1
		assert actual_result.output == [
			cq.checker.ResultLine(
				file = None,
				line = None,
				message = '1 file would be reformatted.',
				is_error = True,
			)
		]
	else:
		assert actual_result.return_code == 0
		assert actual_result.output == []


def test_runner_without_orange_insalled(monkeypatch: Any) -> None:
	def _orange_not_found(cmd: str, options: Any) -> None:
		raise FileNotFoundError

	monkeypatch.setattr(cq.utils, 'run_external_checker', _orange_not_found)
	checker = orange.OrangeChecker()
	test_file = pathlib.Path(__file__).parent / 'data/not-formatted.txt'
	actual_result = checker.run([str(test_file.resolve())])
	assert actual_result.return_code == 0
	assert actual_result.output == [
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = orange.OrangeChecker.ORANGE_NOT_INSTALLED,
			is_error = False,
		)
	]
