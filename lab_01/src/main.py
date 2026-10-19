from toolkit.__main__ import main as run_cli


def main() -> int:
    """Запустить командный интерфейс лабораторной работы."""
    return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
