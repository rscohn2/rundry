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


def get_day(days):
    timestamp = int(
        (datetime.datetime.utcnow() - datetime.timedelta(days=days)).timestamp()
    )
    appid = "bae2645075eb396dccf84f2788ea9122"
    lat = "42.77014807397615"
    lon = "-71.274322339134"
    url = (
        "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
        f"lat={lat}&lon={lon}&units=imperial&dt={timestamp}&appid={appid}"
    )
    print(f"Request {url}")
    data = requests.get(url).json()
    return data


def update(db_file, app_id, lat, long):
    with contextlib.closing(sqlite3.connect(db_file)) as con:
        create_table(con)
        for days in [1, 2, 3, 4, 5]:
            insert_day(con, get_day(days))


def show(db_file):
    with contextlib.closing(sqlite3.connect(db_file)) as con:
        create_table(con)
        cur = con.cursor()
        cur.execute("SELECT * FROM weather")
        rows = cur.fetchall()
        for row in rows:
            print(row)
