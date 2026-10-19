import argparse
import sys

from toolkit.calculator import calculate
from toolkit.constants import EXIT_ERROR, EXIT_SUCCESS
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def _build_parser() -> argparse.ArgumentParser:
    """Настроить аргументы командной строки."""
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Калькулятор и конвертер единиц.",
        allow_abbrev=False,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    calc_parser = subparsers.add_parser(
        "calc",
        help="Вычислить арифметическое выражение.",
    )
    calc_parser.add_argument(
        "expression",
        help="Выражение в кавычках.",
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="Перевести значение между единицами.",
    )
    convert_parser.add_argument(
        "value",
        type=float,
        help="Числовое значение.",
    )
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Исходная единица.",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Целевая единица.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Выполнить команду и вернуть код завершения."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            result = calculate(args.expression)
        else:
            result = convert(
                args.value,
                args.from_unit,
                args.to_unit,
            )

    except ToolkitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR

    print(result)
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
