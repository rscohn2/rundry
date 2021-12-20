# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console

import rundry.weather as weather

app = typer.Typer(
    name="rundry",
    help="Estimate when a home heating oil tank will run dry.",
    add_completion=False,
)
console = Console()

db_file_option = typer.Option("weather.db", help="Weather database file.")
app_id_option = typer.Option("", help="OpenWeather App ID.")


@app.command()
def update(
    db_file: str = db_file_option,
    app_id: str = app_id_option,
    lat: str = typer.Option("42.77014807397615", help="Lattitude for home"),
    long: str = typer.Option("-71.274322339134", help="Longitude for home"),
):
    weather.update(db_file, app_id, lat, long)


@app.command()
def show(
    db_file: str = db_file_option,
):
    weather.show(db_file)


if __name__ == "__main__":
    app()
