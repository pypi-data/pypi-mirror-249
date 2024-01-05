from typing import Any

import cq.checker
import cq.checkers.pylint
import cq.utils


OUTPUT_STRING = '''************* Module test_volume_monitor
dev.py:2: [E0401(import-error), ] Unable to import 'decouple'
file.py: This file is completely wrong
and I want this line to be in output also
'''


def test_runner(monkeypatch: Any) -> None:
	monkeypatch.setattr(cq.utils, 'run_external_checker', lambda cmd, options, stderr: (OUTPUT_STRING, 1))

	checker = cq.checkers.pylint.PylintChecker()

	actual_result = checker.run([])

	assert actual_result.output == [
		cq.checker.ResultLine(
			file = 'dev.py',
			line = 2,
			message = "[E0401(import-error), ] Unable to import 'decouple'",
			is_error = True,
		),
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = 'file.py: This file is completely wrong',
			is_error = False,
		),
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = 'and I want this line to be in output also',
			is_error = False,
		),
	]
