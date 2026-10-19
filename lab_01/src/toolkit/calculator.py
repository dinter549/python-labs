from toolkit.constants import (
    CALCULATOR_OPERATORS,
    NUMBER_CHARACTERS,
    UNARY_OPERATORS,
)
from toolkit.errors import CalculationError


def tokenize(expression: str) -> list[str]:
    """Разбить выражение на числа и операторы.

    Пробельные символы между токенами пропускаются.
    Недопустимые символы и неверная запись числа вызывают
    CalculationError.
    """
    tokens: list[str] = []
    position = 0

    while position < len(expression):
        character = expression[position]

        if character.isspace():
            position += 1
            continue

        if character in CALCULATOR_OPERATORS:
            tokens.append(character)
            position += 1
            continue

        if character in NUMBER_CHARACTERS:
            start = position

            while position < len(expression) and expression[position] in NUMBER_CHARACTERS:
                position += 1

            number = expression[start:position]

            if number == "." or number.count(".") > 1:
                raise CalculationError(
                    f"Неверная запись числа: {number}"
                )

            tokens.append(number)
            continue

        raise CalculationError(
            f"Недопустимый символ: {character}"
        )

    return tokens


def validate(tokens: list[str]) -> None:
    """Проверить порядок токенов, полученных от tokenize.

    Перед числом допускается один унарный знак.
    При нарушении структуры выражения вызвать CalculationError.
    """
    if not tokens:
        raise CalculationError("Пустое выражение")

    expect_operand = True
    unary_sign_seen = False

    for token in tokens:
        if expect_operand:
            if token in UNARY_OPERATORS:
                if unary_sign_seen:
                    raise CalculationError(
                        "Перед числом допускается только один знак"
                    )

                unary_sign_seen = True

            elif token in CALCULATOR_OPERATORS:
                raise CalculationError(
                    f"Ожидалось число, получен оператор: {token}"
                )

            else:
                expect_operand = False
                unary_sign_seen = False

        else:
            if token not in CALCULATOR_OPERATORS:
                raise CalculationError(
                    f"Ожидался оператор, получено число: {token}"
                )

            expect_operand = True

    if expect_operand:
        raise CalculationError("В конце выражения отсутствует число")


def _read_operand(
    tokens: list[str],
    position: int,
) -> tuple[float, int]:
    """Прочитать число с необязательным унарным знаком.

    Вернуть значение и позицию следующего токена.
    Последовательность должна быть предварительно проверена.
    """
    sign = 1.0

    if tokens[position] in UNARY_OPERATORS:
        if tokens[position] == "-":
            sign = -1.0

        position += 1

    value = sign * float(tokens[position])

    return value, position + 1


def evaluate(tokens: list[str]) -> float:
    """Вычислить предварительно проверенное выражение.

    Умножение и деление выполняются раньше сложения и вычитания.
    Деление на ноль вызывает CalculationError.
    """
    first_value, position = _read_operand(tokens, 0)
    terms: list[float] = [first_value]

    while position < len(tokens):
        operator = tokens[position]
        value, position = _read_operand(tokens, position + 1)

        if operator == "*":
            terms[-1] *= value

        elif operator == "/":
            if value == 0.0:
                raise CalculationError("Деление на ноль")

            terms[-1] /= value

        elif operator == "+":
            terms.append(value)

        else:
            terms.append(-value)

    return float(sum(terms))


def calculate(expression: str) -> float:
    """Проверить и вычислить арифметическое выражение."""
    tokens = tokenize(expression)
    validate(tokens)

    return evaluate(tokens)
