# pylint: disable = protected-access
import packaging.version
import pytest
import requirements

import cq.checkers.requirements


version = packaging.version.parse
CHECKER = cq.checkers.requirements.RequirementsSetupCompatiblityChecker


# Mypy error: Untyped decorator makes function "cli_runner" untyped
@pytest.fixture()
def checker() -> CHECKER:
	return CHECKER()


# requirements should be subset of setup
# Mypy error: Untyped decorator makes function "cli_runner" untyped
@pytest.mark.parametrize(
	'requirements, setup, expected_result',
	[
		('a==1.0.0', '', "setup.py: does not contain requirement 'a' that is in requirements.txt"),
		('a==1.2.3', 'a>=1.0.0,<2.0.0', ''),
		(
			'a==2.2.3',
			'a>=1.0.0,<2.0.0',
			"setup.py: requirement 'a' version in requirements.txt (==2.2.3) "
			'does not lie in version of setup.py (>=1.0.0,<2.0.0)',
		),
		('a<5.0.0', 'a<10.0.0', ''),
		('a>2.0.0', 'a>1.0.0', ''),
		('a>1.0.0,<2.0.0', 'a>1.0.0,<2.0.0', ''),
		(
			'a>2.2.0',
			'a<2.0.0',
			"setup.py: requirement 'a' version in requirements.txt (>2.2.0,<=MAX) "
			'does not lie in version of setup.py (>=MIN,<2.0.0)',
		),
		(
			'a>2018.1,<2019.2',
			'a>2019.4',
			"setup.py: requirement 'a' version in requirements.txt (>2018.1,<2019.2) "
			'does not lie in version of setup.py (>2019.4,<=MAX)',
		),
		('a>2018.1,<2019.2', 'a>2017.4', ''),
		('a>2018.1', 'a>2017.4', ''),
		('a<2018.1', 'a<2019.4', ''),
		('a==8', 'a>5,<10', ''),
		('a>=8,<10', 'a>5,<10', ''),
		(
			'a>8',
			'a>5,<10',
			"setup.py: requirement 'a' version in requirements.txt (>8,<=MAX) "
			'does not lie in version of setup.py (>5,<10)',
		),
		(
			'a>12',
			'a>5,<10',
			"setup.py: requirement 'a' version in requirements.txt (>12,<=MAX) "
			'does not lie in version of setup.py (>5,<10)',
		),
		(
			'a>12',
			'a<10',
			"setup.py: requirement 'a' version in requirements.txt (>12,<=MAX) "
			'does not lie in version of setup.py (>=MIN,<10)',
		),
	],
)
def test_requirements_setup_compatibility(
	requirements: str,
	setup: str,
	expected_result: str,
	checker: CHECKER,
) -> None:
	result = checker._check_requirements_setup_compatibility(requirements, setup)
	if expected_result:
		assert result[0].message == expected_result
	else:
		assert not result


def test_version_range_from_specs() -> None:
	specs_str = 'a>=1.0.0,<2.0.0'
	specs = list(requirements.parse(specs_str))[0].specs
	version_range = cq.checkers.requirements.VersionRange.from_specs(specs)  # type: ignore[arg-type]
	assert version_range.lower == version('1.0.0')
	assert version_range.upper == version('2.0.0')
	assert version_range.lower_inclusive
	assert not version_range.upper_inclusive


def test_version_range_from_specs_singleton() -> None:
	specs_str = 'a==1.0.0'
	specs = list(requirements.parse(specs_str))[0].specs
	version_range = cq.checkers.requirements.VersionRange.from_specs(specs)  # type: ignore[arg-type]
	assert version_range.lower == version('1.0.0')
	assert version_range.upper == version('1.0.0')
	assert version_range.lower_inclusive
	assert version_range.upper_inclusive


def test_version_range_subset() -> None:
	vr1 = cq.checkers.requirements.VersionRange(
		version('1.0.0'),
		version('1.1.0'),
		lower_inclusive = True,
		upper_inclusive = False,
	)
	vr2 = cq.checkers.requirements.VersionRange(
		version('1.0.0'),
		version('2.0.0'),
		lower_inclusive = True,
		upper_inclusive = False,
	)

	assert vr1.issubset(vr2)
	assert not vr2.issubset(vr1)

	# vr1 lower is outside of vr2 lower
	vr1.lower = version('0.1.0')
	assert not vr1.issubset(vr2)

	# vr2 lower is not inclusive anymore
	vr1.lower = version('1.0.0')
	vr2.lower_inclusive = False
	assert not vr1.issubset(vr2)
