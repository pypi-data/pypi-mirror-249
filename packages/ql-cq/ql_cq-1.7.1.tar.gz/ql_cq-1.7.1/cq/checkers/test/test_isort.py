import pathlib
import tempfile

import cq.checkers.isort as isort


def test_isort_checker() -> None:
	checker = isort.IsortChecker()
	test_file = pathlib.Path(__file__).parent / 'data/isort.txt'
	with tempfile.TemporaryDirectory() as temp_dir:
		temp_path = pathlib.Path(temp_dir) / 'test.py'
		temp_path.write_text(test_file.read_text(encoding = 'utf-8'), encoding = 'utf-8')
		actual_result = checker.run([str(temp_path.resolve())])
		assert actual_result.return_code == 0
		assert len(actual_result.output) == 1
		assert actual_result.output[0].message == 'Imports are incorrectly sorted and/or formatted.'
		assert not actual_result.output[0].is_error
