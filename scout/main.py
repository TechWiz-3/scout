#!/usr/bin/env python3

import requests
import random
import os
import time
import re
from datetime import datetime as dt

from contextlib import contextmanager

from rich.live import Live
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()

TOKEN = os.getenv("SCOUT_TOKEN")

HEADERS = {'Authorization': 'token ' + TOKEN}

# BASE_URL = "https://api.github.com/search/repositories?q=stars:%3E={}%20language:{}%20topic:hacktoberfest"
BASE_URL = "https://api.github.com/search/repositories?q={}stars:%3C=1000%20language:python%20topic:hacktoberfest"


def get_url():
    standard = console.input("[purple]Shall I use the standard search which gets repos in the 1k stars range? \[y/n]: ")
    if standard.lower() in ("y", "yes", ""):
        max_stars = 1000
    else:
        max_stars = int(console.input("[blue]Star count  range \[5-1000 is ideal]: "))
    lang = console.input("Project language: \[python] ")
    if lang == "":
        lang = "python"
    keyword = console.input("[purple]You can enter a keyword for the search: \[optional] ")
    if keyword != "":
        keyword = f"{keyword} "
    url = BASE_URL.format(keyword, max_stars, lang)
    return url

def request(url):
    page = random.randint(1,3)
    response = requests.get(f"{url}&page={page}", headers=HEADERS)
    response = response.json()
    return response


def get_table_data(response: str) -> list:
    table_data = []
    for project in random.sample(response["items"],min(5, 29)):
        topics = "` `".join(project["topics"])
        topics = f"`{topics}`"
        topics = Markdown(topics, style="dim")
        stars = "{:,}".format(project["stargazers_count"])
    #    stars = f":star: {stars}"
        issues = "{:,}".format(project["open_issues_count"])
        time = project["updated_at"]
        #day = re.match(time, r"^[0-9]{4}-[0-9]{2}-[0-9]{2}")
        time = time[:10]
        time = dt.strptime(time, "%Y-%m-%d")
        if time.date() == dt.today().date():
            time = "Today"
        else:
            delta = dt.today().date() - time.date()
        if delta.days == 1:
            time = f"{str(delta.days)} day"
        else:
            time = f"{str(delta.days)} days"
        table_data.append(
                    [
                        project["name"], project["description"],
                        str(stars), str(issues), topics, time
                    ]
                )
    return table_data


def display_table(table_data):
    table = Table(padding=(0,1,1,1))
    table.add_column("Project", header_style="bold cyan", style="bold cyan")
    table.add_column("Description", header_style="bold green", style="italic green")
    table.add_column("Stars", header_style="bold yellow", style="yellow")
    table.add_column("Issues", header_style="bold grey66", style="grey66")
    table.add_column("Tags", header_style="bold")
    table.add_column("Last updated", header_style="red bold", style="red")
    table.add_row(*table_data[0])
    with Live(table, console=console, refresh_per_second=4):
        for row in table_data[1:]:
            table.add_row(*row)
            time.sleep(0.5)


def cli() -> None:
    url = get_url()
    console.clear()
    response = request(url)
    table_data = get_table_data(response)
    display_table(table_data)


if __name__ == "__main__":
    cli()
