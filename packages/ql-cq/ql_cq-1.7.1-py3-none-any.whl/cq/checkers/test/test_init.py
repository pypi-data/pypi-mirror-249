import pathlib

import py
import pytest

import cq.checkers.init as checker


def make_module(path: pathlib.Path, module_name: str = 'module', include_init: bool = False) -> pathlib.Path:
	module = path / module_name
	module.mkdir()
	(module / 'main.py').touch()
	if include_init:
		(module / '__init__.py').touch()
	return module


@pytest.mark.parametrize('include_init', [True, False])
def test_simple_module(tmpdir: py.path.local, include_init: bool) -> None:
	''' Top-level module can be with or without __init__.py '''
	tmp = pathlib.Path(tmpdir)
	module = make_module(tmp, include_init = include_init)
	errors = checker.find_missing_inits(module)
	assert list(errors) == []


def test_module_with_subdirectory(tmpdir: py.path.local) -> None:
	''' Should ignore subdirectories as long as they don't have *.py file in them '''
	tmp = pathlib.Path(tmpdir)
	module = make_module(tmp)
	subdirectory = module / 'subdir'
	subdirectory.mkdir()
	(subdirectory / 'hello.txt').touch()
	errors = checker.find_missing_inits(module)
	assert list(errors) == []


@pytest.mark.parametrize('include_init', [True, False])
@pytest.mark.parametrize('submodule_name', ['submodule', '.hidden'])
def test_module_with_submodule(tmpdir: py.path.local, include_init: bool, submodule_name: str) -> None:
	''' Submodules must have __init__.py, should ignore hidden directories '''
	tmp = pathlib.Path(tmpdir)
	module = make_module(tmp)
	submodule = make_module(module, module_name = submodule_name, include_init = include_init)
	errors = checker.find_missing_inits(module)
	if include_init or submodule_name == '.hidden':
		assert list(errors) == []
	else:
		assert list(errors) == [submodule]


def test_deep_nested_submodule(tmpdir: py.path.local) -> None:
	''' Should recursively check submodules (even those without __init__.py) '''
	tmp = pathlib.Path(tmpdir)
	module = make_module(tmp)
	level_1_1 = make_module(module, module_name = 'level_1_1', include_init = True)
	level_1_2 = make_module(module, module_name = 'level_1_2', include_init = False)
	level_2_1 = make_module(level_1_1, module_name = 'level_2_1', include_init = True)
	level_2_2 = make_module(level_1_1, module_name = 'level_2_2', include_init = False)
	level_2_3 = make_module(level_1_2, module_name = 'level_2_3', include_init = False)
	level_3_1 = make_module(level_2_1, module_name = 'level_3_1', include_init = False)
	errors = checker.find_missing_inits(module)
	assert set(errors) == {level_1_2, level_2_2, level_2_3, level_3_1}
