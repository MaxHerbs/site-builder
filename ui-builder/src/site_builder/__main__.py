"""Interface for ``python -m site_builder``."""

import logging

import typer

from ._version import __version__
from .site_builder import site_builder

app = typer.Typer(no_args_is_help=True)


def setup_logging(logging_level: str):
    """
    Sets up the logging level based on the CLI param
    """
    level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    level = level_map.get(logging_level.lower(), logging.ERROR)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    )

    logging.debug("Logging is set up.")


def version_callback(value: bool):
    if value:
        typer.echo(f"Hive-Controller-IOC Version: {__version__}")
        raise typer.Exit()


@app.command()
def run(config_path: str = typer.Option(..., help="Path to the config file")):
    """
    Run the site builder
    """
    site_builder(config_path)


@app.callback()
def main(version: bool = typer.Option(None, "--version", callback=version_callback)):
    """
    Builder entry point
    """
    pass


if __name__ == "__main__":
    app()
