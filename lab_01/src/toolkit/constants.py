LENGTH_FACTORS: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

MASS_FACTORS: dict[str, float] = {
    "g": 1.0,
    "kg": 1000.0,
}

UNIT_GROUPS: dict[str, str] = {
    "mm": "length",
    "cm": "length",
    "m": "length",
    "km": "length",
    "g": "mass",
    "kg": "mass",
    "c": "temperature",
    "f": "temperature",
    "k": "temperature",
}

LINEAR_FACTORS: dict[str, dict[str, float]] = {
    "length": LENGTH_FACTORS,
    "mass": MASS_FACTORS,
}

CELSIUS_TO_KELVIN_OFFSET: float = 273.15
FAHRENHEIT_OFFSET: float = 32.0
FAHRENHEIT_TO_CELSIUS_SCALE: float = 5.0 / 9.0

ABSOLUTE_ZERO: dict[str, float] = {
    "c": -273.15,
    "f": -459.67,
    "k": 0.0,
}

CALCULATOR_OPERATORS: str = "+-*/"
NUMBER_CHARACTERS: str = "0123456789."
UNARY_OPERATORS: str = "+-"

EXIT_SUCCESS: int = 0
EXIT_ERROR: int = 2
