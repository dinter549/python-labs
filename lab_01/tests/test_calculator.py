import pytest

from toolkit.calculator import calculate, tokenize, validate
from toolkit.errors import CalculationError


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("12+3", ["12", "+", "3"]),
        (
            " 12.5 + 2 * -3 ",
            ["12.5", "+", "2", "*", "-", "3"],
        ),
        ("10/4", ["10", "/", "4"]),
        (".5+5.", [".5", "+", "5."]),
        ("1 2", ["1", "2"]),
        ("", []),
        (" \t\n", []),
    ],
)
def test_tokenize(expression: str, expected: list[str]) -> None:
    """Выражение правильно разбивается на токены."""
    assert tokenize(expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "2+a",
        ".",
        "1.2.3",
        "2&3",
        "3,5",
    ],
)
def test_tokenize_invalid_input(expression: str) -> None:
    """Недопустимые символы и числа вызывают ошибку."""
    with pytest.raises(CalculationError):
        tokenize(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "2+3",
        "2+3*4",
        "2*-3",
        "1+-2",
        "2--3",
        "+3",
        "-3",
        ".5+5.",
        "1/0",
    ],
)
def test_validate_correct_expression(expression: str) -> None:
    """Правильно составленные выражения проходят валидацию."""
    tokens = tokenize(expression)

    validate(tokens)


@pytest.mark.parametrize(
    "expression",
    [
        "",
        " ",
        "2+",
        "*2",
        "2*/3",
        "2 3",
        "--3",
        "2*--3",
        "+",
        "2//3",
    ],
)
def test_validate_invalid_expression(expression: str) -> None:
    """Неправильная структура выражения вызывает ошибку."""
    tokens = tokenize(expression)

    with pytest.raises(CalculationError):
        validate(tokens)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2+3", 5.0),
        ("9-4", 5.0),
        ("3*4", 12.0),
        ("10/4", 2.5),
        ("2+3*4", 14.0),
        ("8/4*2", 4.0),
        ("8-3-2", 3.0),
        ("2*-3", -6.0),
        ("1+-2", -1.0),
        ("2--3", 5.0),
        ("-3", -3.0),
        ("+3", 3.0),
        (".5+5.5", 6.0),
        ("2 + 3 * 4 - 10 / 2", 9.0),
        ("2-3*4", -10.0),
    ],
)
def test_calculate(expression: str, expected: float) -> None:
    """Калькулятор правильно вычисляет допустимые выражения."""
    assert calculate(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    "expression",
    [
        "",
        "2+a",
        "2+",
        "2*/3",
        "1/0",
        "1/-0",
        "1/0.0",
        "2 3",
        "--3",
    ],
)
def test_calculate_invalid_expression(expression: str) -> None:
    """Ошибочное выражение вызывает CalculationError."""
    with pytest.raises(CalculationError):
        calculate(expression)
