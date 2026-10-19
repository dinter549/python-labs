class ToolkitError(Exception):
    """Базовая ошибка утилит."""


class ConversionError(ToolkitError):
    """Ошибка преобразования единиц."""


class CalculationError(ToolkitError):
    """Ошибка разбора или вычисления выражения."""
