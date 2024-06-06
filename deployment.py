import asyncio
import importlib
import os
import subprocess
import sys
from time import sleep
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
    "db": ["docker-compose -f docker-compose.yml up -d db"],

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
def migrate(app: str | None = None, init: bool = False):
    run_db(test=False)
    if init:
        run_commands(
            [
                f"aerich {f'--app {app}' if app else ''} init  -t src.config.TORTOISE_CONFIG  --location src/migrations "
            ]
        )
        sleep(1)
        run_commands([f"aerich {f'--app {app}' if app else ''} init-db"])

    run_commands([f"aerich {f'--app {app}' if app else ''} migrate"])


@app.command()
def migrate_manual(migration: str):
    class MigrationApplier:
        def __init__(self, migration: str):
            self.migration = migration

        def find_migration(self):
            """
            Find the migration file in the migrations directory
            Returns:

            """
            migrations = os.listdir("src/migrations/manual/")
            for migration in migrations:
                if migration.startswith(self.migration) or self.migration in migration:
                    return migration
            raise FileNotFoundError(f"Migration {self.migration} not found")

        def import_migration(self):
            migration = self.find_migration()
            module = importlib.import_module(f"src.migrations.manual.{migration.replace('.py', '')}")
            return module

        def get_migration_class(self):
            module = self.import_migration()
            for attr in dir(module):
                if "Migration" in attr and attr != "BaseMigration":
                    return getattr(module, attr)
            raise AttributeError(f"Migration class not found in {module}")

        def apply(self):
            from src.config.api_config import ApiConfig

            migration_class = self.get_migration_class()
            migration = migration_class(ApiConfig().DATABASE_URL)
            asyncio.run(migration.run())

    return MigrationApplier(migration).apply()


@app.command()
def bootstrap():
    run_commands(["docker-compose down"])
    run_commands(["docker-compose up -d"])
    # migrate()


if __name__ == "__main__":
    app()
