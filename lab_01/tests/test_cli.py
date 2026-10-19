import subprocess
import sys
from pathlib import Path

import pytest


def run_cli(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    """Запустить toolkit отдельным процессом и получить результат."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *arguments],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["calc", "2+3*4"], 14.0),
        (
            ["convert", "1000", "--from", "mm", "--to", "m"],
            1.0,
        ),
        (["calc", "--", "-2+3"], 1.0),
    ],
)
def test_cli_success(
    arguments: list[str],
    expected: float,
) -> None:
    """Успешная команда выводит результат и возвращает код 0."""
    process = run_cli(arguments)

    assert process.returncode == 0
    assert process.stderr == ""
    assert float(process.stdout.strip()) == pytest.approx(expected)


def test_cli_help() -> None:
    """Справка перечисляет команды и завершается с кодом 0."""
    process = run_cli(["--help"])

    assert process.returncode == 0
    assert process.stderr == ""
    assert "calc" in process.stdout
    assert "convert" in process.stdout


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["calc", "1/0"],
        ["calc", ""],
        ["convert", "hello", "--from", "m", "--to", "cm"],
        ["convert", "1", "--from", "kg", "--to", "m"],
        ["convert", "1", "--from", "unknown", "--to", "m"],
        ["convert", "-1", "--from", "k", "--to", "c"],
        ["convert", "nan", "--from", "m", "--to", "cm"],
    ],
)
def test_cli_error(arguments: list[str]) -> None:
    """Ошибочная команда пишет в stderr и возвращает код 2."""
    process = run_cli(arguments)

    assert process.returncode == 2
    assert process.stdout == ""
    assert process.stderr.strip() != ""
    assert "Traceback" not in process.stderr
