import pytest

from toolkit.converter import convert
from toolkit.errors import ConversionError


def test_millimeters_to_meters() -> None:
    """Тысяча миллиметров равна одному метру."""
    result = convert(1000.0, "mm", "m")

    assert result == pytest.approx(1.0)


def test_unit_names_are_case_insensitive() -> None:
    """Единицы в верхнем регистре принимаются."""
    result = convert(1.0, "KM", "M")

    assert result == pytest.approx(1000.0)


def test_unknown_unit_raises_error() -> None:
    """Неизвестная единица вызывает ошибку."""
    with pytest.raises(ConversionError):
        convert(1.0, "unknown", "m")


def test_kilograms_to_grams() -> None:
    """Полтора килограмма равны 1500 граммам."""
    result = convert(1.5, "kg", "g")

    assert result == pytest.approx(1500.0)


def test_grams_to_kilograms() -> None:
    """250 граммов равны четверти килограмма."""
    result = convert(250.0, "g", "kg")

    assert result == pytest.approx(0.25)


def test_incompatible_units_raise_error() -> None:
    """Перевод между массой и длиной запрещён."""
    with pytest.raises(ConversionError):
        convert(1.0, "kg", "m")


def test_unknown_target_unit_raises_error() -> None:
    """Неизвестная целевая единица вызывает ошибку."""
    with pytest.raises(ConversionError):
        convert(1.0, "m", "unknown")


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (0.0, "c", "f", 32.0),
        (32.0, "f", "c", 0.0),
        (273.15, "k", "c", 0.0),
        (-273.15, "c", "k", 0.0),
        (-459.67, "f", "k", 0.0),
        (0.0, "k", "f", -459.67),
    ],
)
def test_temperature_conversion(value: float, from_unit: str, to_unit: str, expected: float) -> None:
    """Температура правильно переводится между шкалами."""
    result = convert(value, from_unit, to_unit)

    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit"),
    [
        (-274.0, "c", "k"),
        (-460.0, "f", "c"),
        (-1.0, "k", "f"),
        (-1.0, "k", "k"),
    ],
)
def test_temperature_below_absolute_zero_raises_error(
    value: float,
    from_unit: str,
    to_unit: str,
) -> None:
    """Температура ниже абсолютного нуля запрещена."""
    with pytest.raises(ConversionError):
        convert(value, from_unit, to_unit)


def test_temperature_and_length_are_incompatible() -> None:
    """Температуру нельзя перевести в длину."""
    with pytest.raises(ConversionError):
        convert(10.0, "c", "m")
