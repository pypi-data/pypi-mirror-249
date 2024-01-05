from typing import List

import pytest

import cq.checkers.regex


def _check_grammar_nazi(s: str) -> List[str]:
	return list(cq.checkers.regex.check_line(s, s, cq.checkers.regex.GrammarNaziChecker.RULES))


def test_exists() -> None:
	assert _check_grammar_nazi("Yo dawg, dis is Queen's English!") == []
	assert _check_grammar_nazi('Trade does NOT exists') == [  # grammar_checker: disable = 3rd-person-singular
		'Use "does not exist", not "does not exists". '  # grammar_checker: disable = 3rd-person-singular
		'The "does" verb already is in third person singular.'
	]
	assert _check_grammar_nazi('Trade may not exists') == [  # grammar_checker: disable = 3rd-person-singular
		'Use "may not exist", not "may not exists". '  # grammar_checker: disable = 3rd-person-singular
		'The "may" verb already is in third person singular.'
	]


def test_happend() -> None:  # grammar_checker: disable = happend
	assert _check_grammar_nazi('This can happend only ...') == [  # grammar_checker: disable = happend
		'"happend" is not a word. '  # grammar_checker: disable = happend
		'You either mean "happen" (present tense) or "happened" (past tense).'
	]


def test_it_self() -> None:
	assert _check_grammar_nazi('await self.x()') == []


def test_single() -> None:
	assert cq.checkers.regex.clobber_string_literals("print('hi')") == "print('..')"


def test_double() -> None:
	assert cq.checkers.regex.clobber_string_literals('print("hi")') == 'print("..")'


def test_escape_single() -> None:
	assert cq.checkers.regex.clobber_string_literals(''' q = '\\'' ''') == " q = '..' "


def test_escape_double() -> None:
	assert cq.checkers.regex.clobber_string_literals(''' q = "\\"" ''') == ' q = ".." '


def _check_dumb_style_checker(s: str) -> List[str]:
	return list(cq.checkers.regex.check_line(s, s, cq.checkers.regex.DumbStyleChecker.RULES))


@pytest.mark.parametrize(
	'source',
	(
		'a = 1',
		'a == 1',
		'a >= 1',
		'a <= 1',
		'a != 1',
		'a += 1',
		'a := 1',
		'a =',
	),
)
def test_spaces_around_equals_sign_negative(source: str) -> None:
	assert _check_dumb_style_checker(source) == []


@pytest.mark.parametrize(
	'source',
	(
		'print_this("hi", end="!")',
		'a=1',
		'a =1',
		'a= 1',
	),
)
def test_spaces_around_equals_sign_positive(source: str) -> None:
	result = _check_dumb_style_checker(source)
	assert len(result) == 1
	assert result[0].startswith('Put exactly one space before and after `=`')


@pytest.mark.parametrize(
	'source, operator',
	(
		('a!=1', '!='),
		('a !=1', '!='),
		('a>=1', '>='),
		('a== 1', '=='),
	),
)
def test_spaces_around_other_operators_positive(source: str, operator: str) -> None:
	result = _check_dumb_style_checker(source)
	assert len(result) == 1
	assert result[0].startswith(f'Put exactly one space before and after `{operator}`')


@pytest.mark.parametrize(
	'source',
	(
		'variable1 = ...',
		'variable2 = ...',
		'variable4 = ...',
		# These lines are ignore as an exception in regex
		'OAuth2Authenticator',
		'oauth2client.client',
	),
)
def test_number_in_names_negative(source: str) -> None:
	assert _check_dumb_style_checker(source) == []


@pytest.mark.parametrize(
	'source, number',
	(
		('def convert2string() -> str:', '2'),
		('def test4missing_rules() -> None:', '4'),
		('convert2price = []', '2'),
	),
)
def test_number_in_names_positive(source: str, number: str) -> None:
	result = _check_dumb_style_checker(source)
	assert len(result) == 1

	verb = 'to' if number == '2' else 'for'
	assert result[0].startswith(f'Do not spell `{verb}` as the digit `{number}`')


@pytest.mark.parametrize(
	'source',
	(
		'some_print(some_stuff)',
		'print(with_disable) # dumb_style_checker:disable = print-statement',
	),
)
def test_print_statement_negative(source: str) -> None:
	assert _check_dumb_style_checker(source) == []


@pytest.mark.parametrize(
	'source',
	(
		' print(some_stuff)',
		' print("other stuff")',
	),
)
def test_print_statement_positive(source: str) -> None:
	result = _check_dumb_style_checker(source)
	assert len(result) == 1
	assert result[0].startswith(
		'It seems that you have forgotten about a print statement. '
		'If this is intentional, disable this check by # dumb_style_checker:disable = print-statement'
	)


def test_operators_at_line_start() -> None:
	source = '''
assert (
	{
		'key': 42,
	}
	== test_func()
)
	'''
	assert _check_dumb_style_checker(source) == []
