from typing import Any

import cq.checker
import cq.checkers.pyflakes
import cq.utils


OUTPUT_STRING = '''file.py:3: dictionary key 'test' repeated with different values
file.py: This file is completely wrong
and I want this line to be in output also'''


def test_runner(monkeypatch: Any) -> None:
	monkeypatch.setattr(cq.utils, 'run_external_checker', lambda cmd, options: (OUTPUT_STRING, 1))

	checker = cq.checkers.pyflakes.PyflakesExtChecker()

	actual_result = checker.run([])

	assert actual_result.output == [
		cq.checker.ResultLine(
			file = 'file.py',
			line = 3,
			message = "dictionary key 'test' repeated with different values",
			is_error = True,
		),
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = 'file.py: This file is completely wrong',
			is_error = True,
		),
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = 'and I want this line to be in output also',
			is_error = True,
		),
	]
