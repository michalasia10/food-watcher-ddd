import subprocess
import sys
from typing import Optional

import typer
from typer import progressbar

app = typer.Typer()

COMMANDS: dict[str, list[str]] = {
    "test": [
        "docker-compose -f docker-compose.testdb.yml stop test_db",
        "docker-compose -f docker-compose.testdb.yml up -d test_db",
        "pytest tests/ -s OPTIONAL_ARGS",
        "docker-compose -f docker-compose.testdb.yml stop test_db"
    ],
    "test_db": ["docker-compose -f docker-compose.testdb.yml up -d test_db"],

}


def run_commands(command_list, optional_args=None):
    command: str
    with progressbar(command_list, label="Running commands") as commands:
        for idx, command in enumerate(commands):
            if optional_args:
                command = command.replace("OPTIONAL_ARGS", optional_args)
            else:
                command = command.replace("OPTIONAL_ARGS", "")
            typer.echo("\n" * 2 + "#" * 25 + " " * 5 + f"{idx + 1}/{len(command_list)}" + " " * 5 + "#" * 41)
            typer.echo(f"{typer.style('Run command', fg=typer.colors.YELLOW, bold=True)}:"
                       f" command'{command}")
            typer.echo("#" * 80)
            result = subprocess.run(command, shell=True)
            if result.returncode != 0:
                typer.echo("\n" * 2 + "#" * 80)
                typer.echo(f"{typer.style('Error', fg=typer.colors.RED, bold=True)}: command {command}")
                typer.echo("#" * 80)
                sys.exit(1)

            typer.echo("\n" * 2 + "#" * 80)
            typer.echo(f"{typer.style('End command:', fg=typer.colors.GREEN, bold=True)}: {command}")
            typer.echo("#" * 80)


@app.command()
def test(test_case: Optional[str] = None, pytest_args: Optional[str] = None):
    _args = ""
    if test_case:
        _args += f" -k {test_case}"
    if pytest_args:
        _args += f" {pytest_args}"
    run_commands(COMMANDS["test"], _args)


@app.command()
def run_db(test: Optional[bool] = False):
    if test:
        run_commands(COMMANDS["test_db"])
    else:
        run_commands(COMMANDS["db"])


@app.command()
def run_migrations(name: str):
    run_commands([f"alembic revision --autogenerate -m '{name}'"])


@app.command()
def migrate():
    run_commands(["aerich --app auth init -s src -t src.config.TORTOISE_CONFIG  --location src.migrations "])
    run_commands(["aerich --app auth init-db"])
    run_commands(["aerich --app auth migrate"])


@app.command()
def bootstrap():
    run_commands(["docker-compose down"])
    run_commands(["docker-compose up -d"])
    # migrate()


if __name__ == "__main__":
    app()
