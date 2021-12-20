"""Manage weather data."""

import contextlib
import datetime
import json
import sqlite3

import requests


def create_table(con):
    with con as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS weather"
            " (timestamp DATETIME primary key,temperature NUMERIC,"
            " humidity NUMERIC, uvi NUMERIC)"
        )


def insert_day(con, day):
    for hour in day["hourly"]:
        with con as cur:
            cur.execute(
                "INSERT OR IGNORE INTO weather(timestamp,temperature,humidity,uvi) VALUES(?,?,?,?)",
                (hour["dt"], hour["temp"], hour["humidity"], hour["uvi"]),
            )


def get_day(days, appid, lat, long):
    timestamp = int(
        (datetime.datetime.utcnow() - datetime.timedelta(days=days)).timestamp()
    )
    url = (
        "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
        f"lat={lat}&lon={long}&units=imperial&dt={timestamp}&appid={appid}"
    )
    data = requests.get(url).json()
    return data


def update(db_file, appid, lat, long):
    with contextlib.closing(sqlite3.connect(db_file)) as con:
        create_table(con)
        for days in [1, 2, 3, 4, 5]:
            insert_day(con, get_day(days, appid, lat, long))


def show(db_file):
    with contextlib.closing(sqlite3.connect(db_file)) as con:
        create_table(con)
        cur = con.cursor()
        cur.execute("SELECT * FROM weather")
        rows = cur.fetchall()
        for row in rows:
            print(row)
