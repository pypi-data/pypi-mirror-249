import os

import py

import cq.utils


def test_simple_module(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('module').join('__init__.py')
	f.write('')
	module_name = os.path.dirname(str(f))
	gen = cq.utils.get_path_generator([module_name])
	assert list(gen) == [module_name]


def test_python_file(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('module').join('test.py')
	f.write('')
	module_name = str(f)
	gen = cq.utils.get_path_generator([module_name])
	assert list(gen) == [module_name]


def test_directory_of_python_files(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('module').join('test.py')
	f.write('')
	g = tmpdir.join('module').join('test2.py')
	g.write('')
	path1 = str(f)
	path2 = str(g)
	gen = cq.utils.get_path_generator([os.path.dirname(path1)])
	assert set(gen) == {path1, path2}


def test_combination(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('module').join('test.py')
	f.write('')
	g = tmpdir.join('module').mkdir('pymodule').join('__init__.py')
	g.write('')

	path1 = str(f)
	dir1 = os.path.dirname(path1)
	path2 = str(g)
	dir2 = os.path.dirname(path2)
	gen = cq.utils.get_path_generator([dir1, dir2])
	assert set(gen) == {path1, dir2}


def test_empty(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('module').join('empty_file')
	f.write('')

	path = str(f)
	gen = cq.utils.get_path_generator([path])
	assert list(gen) == []


def test_hidden_file(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('module').join('.hidden.py')
	f.write('')

	path = str(f)
	gen = cq.utils.get_path_generator([path])
	assert list(gen) == []


def test_hidden_dir(tmpdir: py.path.local) -> None:
	f = tmpdir.mkdir('.module').mkdir('sub').join('hidden.py')
	f.write('')

	path = str(f)
	gen = cq.utils.get_path_generator([path])
	assert list(gen) == []
