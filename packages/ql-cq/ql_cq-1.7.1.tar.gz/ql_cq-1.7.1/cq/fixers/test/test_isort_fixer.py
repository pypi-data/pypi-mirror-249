import pathlib
import tempfile

import cq.fixers.isort_fixer as isort


def test_isort_fixer() -> None:
	fixer = isort.IsortFixer()
	test_path = pathlib.Path(__file__).parent / 'data/isort-test.txt'
	result_path = pathlib.Path(__file__).parent / 'data/isort-result.txt'
	with tempfile.TemporaryDirectory() as temp_dir:
		temp_path = pathlib.Path(temp_dir) / 'test.py'
		temp_path.write_text(test_path.read_text(encoding = 'utf-8'), encoding = 'utf-8')
		fixer.run([str(temp_path)])
		assert temp_path.read_text(encoding = 'utf-8') == result_path.read_text(encoding = 'utf-8')
