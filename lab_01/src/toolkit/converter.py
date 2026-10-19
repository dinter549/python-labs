from math import isfinite

from toolkit.constants import (
    ABSOLUTE_ZERO,
    CELSIUS_TO_KELVIN_OFFSET,
    FAHRENHEIT_OFFSET,
    FAHRENHEIT_TO_CELSIUS_SCALE,
    LINEAR_FACTORS,
    UNIT_GROUPS,
)
from toolkit.errors import ConversionError


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Перевести температуру между проверенными единицами c, f и k."""
    if value < ABSOLUTE_ZERO[from_unit]:
        raise ConversionError("Температура ниже абсолютного нуля")

    if value == ABSOLUTE_ZERO[from_unit]:
        kelvin = ABSOLUTE_ZERO["k"]
    elif from_unit == "c":
        kelvin = value + CELSIUS_TO_KELVIN_OFFSET
    elif from_unit == "f":
        celsius = (value - FAHRENHEIT_OFFSET) * FAHRENHEIT_TO_CELSIUS_SCALE
        kelvin = celsius + CELSIUS_TO_KELVIN_OFFSET
    else:
        kelvin = value

    if to_unit == "c":
        result = kelvin - CELSIUS_TO_KELVIN_OFFSET
    elif to_unit == "f":
        result = (
            (kelvin - CELSIUS_TO_KELVIN_OFFSET)
            / FAHRENHEIT_TO_CELSIUS_SCALE
            + FAHRENHEIT_OFFSET
        )
    else:
        result = kelvin

    return float(result)


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Перевести длину, массу или температуру.

    Нечисловые специальные значения, неизвестные и несовместимые
    единицы, а также температура ниже абсолютного нуля
    вызывают ConversionError.
    """

    if not isfinite(value):
        raise ConversionError("Значение должно быть конечным числом")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in UNIT_GROUPS:
        raise ConversionError(f"Неизвестная единица: {from_unit}")

    if to_unit not in UNIT_GROUPS:
        raise ConversionError(f"Неизвестная единица: {to_unit}")

    from_group = UNIT_GROUPS[from_unit]
    to_group = UNIT_GROUPS[to_unit]

    if from_group != to_group:
        raise ConversionError(
            f"Несовместимые единицы: {from_unit} и {to_unit}"
        )

    if from_group == "temperature":
        return _convert_temperature(value, from_unit, to_unit)

    factors = LINEAR_FACTORS[from_group]

    value_in_base_unit = value * factors[from_unit]
    result = value_in_base_unit / factors[to_unit]

    return float(result)
