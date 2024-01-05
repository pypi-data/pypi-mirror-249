from typing import Any, Tuple
import os

import pytest

import cq.checkers.git
import cq.utils


CHECKER = cq.checkers.git.BranchNameChecker


@pytest.fixture
def branch_name_checker() -> CHECKER:
	return CHECKER()


def test_correct_branch_name_env(monkeypatch: Any, branch_name_checker: CHECKER) -> None:
	monkeypatch.setattr(os, 'environ', {'CI_COMMIT_REF_NAME': 'feature/cool_new_feature'})

	result = branch_name_checker.run([])
	assert result.return_code == 0


def test_correct_branch_name_git(monkeypatch: Any, branch_name_checker: CHECKER) -> None:
	def runner(cmd: str, _options: Any) -> Tuple[str, int]:
		if cmd != 'git':
			assert False

		return ('master', 0)

	monkeypatch.setattr(cq.utils, 'run_external_checker', runner)

	result = branch_name_checker.run([])
	assert result.return_code == 0


def test_incorrect_branch_name_env(monkeypatch: Any, branch_name_checker: CHECKER) -> None:
	monkeypatch.setattr(os, 'environ', {'CI_COMMIT_REF_NAME': 'incorrectly_named_branch'})

	result = branch_name_checker.run([])
	assert result.return_code == 1
