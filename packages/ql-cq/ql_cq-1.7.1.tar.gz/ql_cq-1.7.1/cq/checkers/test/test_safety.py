from typing import Any, Tuple
import sys

import cq.checker
import cq.checkers.safety
import cq.utils


NO_CONNECTION_ERROR = 'socket.gaierror: [Errno -3] Temporary failure in name resolution'


def pip_helper(package: str, uninstall: bool = False) -> Tuple[str, int]:
	options = ['-m', 'pip', 'uninstall', '-y', package] if uninstall else ['-m', 'pip', 'install', package]

	return cq.utils.run_external_checker(
		sys.executable,
		options,
	)


def test_runner(monkeypatch: Any) -> None:
	# first make sure insecure-package is not currently installed
	_, return_code = pip_helper('insecure-package', uninstall = True)
	assert return_code == 0

	checker = cq.checkers.safety.SafetyChecker()

	secure_result = checker.run([])
	assert secure_result.return_code == 0
	assert secure_result.output == []

	# install insecure-package
	_, return_code = pip_helper('insecure-package')
	assert return_code == 0

	insecure_result = checker.run([])
	assert insecure_result.return_code == 64
	assert insecure_result.output == [
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = 'package: insecure-package, affected: <0.2.0, installed: 0.1.0',
			is_error = True,
		)
	]

	# connection error case
	monkeypatch.setattr(cq.utils, 'run_external_checker', lambda cmd, options: (NO_CONNECTION_ERROR, 1))
	connection_error_result = checker.run([])

	assert connection_error_result.return_code == 0
	assert connection_error_result.output == [
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = cq.checkers.safety.SAFETY_CONNECTION_WARNING,
			is_error = False,
		)
	]

	# generic error case
	monkeypatch.setattr(cq.utils, 'run_external_checker', lambda cmd, options: ('', 7))
	generic_error_result = checker.run([])
	assert generic_error_result.return_code == 7
	assert generic_error_result.output == [
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = cq.checkers.safety.SAFETY_OTHER_ERROR,
			is_error = True,
		)
	]

	# decode error case
	monkeypatch.setattr(cq.utils, 'run_external_checker', lambda cmd, options: ('this is not json', 64))
	decode_error_result = checker.run([])
	assert decode_error_result.return_code == 64
	assert decode_error_result.output == [
		cq.checker.ResultLine(
			file = None,
			line = None,
			message = cq.checkers.safety.SAFETY_DECODE_ERROR,
			is_error = True,
		)
	]

	monkeypatch.undo()

	# finally uninstall insecure-package
	_, return_code = pip_helper('insecure-package', uninstall = True)
	assert return_code == 0
