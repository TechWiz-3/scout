#!/usr/bin/env python3
from turtle import color
from typing import Dict

import requests
import random
import os
import time
import re
import sys
from datetime import datetime as dt

from contextlib import contextmanager
import argparse
from rich.live import Live
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from rich.markdown import Markdown

console = Console()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--standard', action='store_true', required=False,
    help='Run the standard query for Python repos under 1k stars'
)

parser.add_argument(
    '--forks', action='store_true', required=False,
    help='Show repos Forks'
)

parser.add_argument(
    '--nocolor', action='store_true', required=False,
    help='Default color theme'
)


args = parser.parse_args()
noColor = args.nocolor

TOKEN = os.getenv("SCOUT_TOKEN")

# BASE_URL = "https://api.github.com/search/repositories?q=stars:%3E={}%20language:{}%20topic:hacktoberfest"
BASE_URL = "https://api.github.com/search/repositories?q={}stars:%3C={}%20language:{}%20topic:hacktoberfest"

def get_headers() -> dict[str, str]:
    if not TOKEN:
        print("You aren't using a Github token, this may result in ratelimits.")
    return {'Authorization': 'token ' + TOKEN if TOKEN else ""}


def print_welcome_message() -> None:
    if noColor:
        rule = Rule(
        '[b]Your personal opensource Scout',
        align="center"
    )
    else:
        rule = Rule(
        '[b]Your personal opensource [purple]Scout',
        align="center",
        style="yellow"
    )

    console.print(rule)
    print("")


def get_url():
    if args.standard:
        keyword = ''
        max_stars = '1000'
        lang = 'python'
    else:
        try:
            if noColor:
                standard = console.input(
                "Shall I use the standard search which gets repos in the 1k stars range? \[y/n]: ")
                keyword = console.input("You can enter a keyword for the search: \[optional] ")
            else:
                standard = console.input(
                "[purple]Shall I use the standard search which gets repos in the 1k stars range? \[y/n]: ")
                keyword = console.input("[purple]You can enter a keyword for the search: \[optional] ")
            lang = console.input("Project language: \[python] ")

        except KeyboardInterrupt:
            print('\nFarewell my friend, beware the crickets.\n')
            sys.exit(1)

        else:
            if standard.lower() in ("y", "yes", ""):
                max_stars = 1000
            else:
                if noColor:
                    max_stars = int(console.input("Star count  range \[5-1000 is ideal]: "))
                else:
                    max_stars = int(console.input("[blue]Star count  range \[5-1000 is ideal]: "))
                


            if lang == "":
                lang = "python"

            if keyword != "":
                keyword = f"{keyword} "

    url = BASE_URL.format(keyword, max_stars, lang)
    return url


def request(url):
    page = random.randint(1, 3)
    response = requests.get(f"{url}&page={page}", headers=get_headers())
    status_code = response.status_code

    response_json = response.json()

    if response_json.get("items") is None:
        if status_code == 403:
            print("API rate limit exceeded, use the Github token")
        elif status_code == 401:
            print("GitHub Token invalid!")
        console.print(f"\n{str(response_json)}")  # print response from gh api
        exit()

    return response_json


def get_table_data(response: str) -> list:
    table_data = []
    for project in random.sample(response["items"], min(5, 29)):
        topics = "` `".join(project["topics"])
        topics = f"`{topics}`"
        topics = Markdown(topics, style="dim")
        stars = "{:,}".format(project["stargazers_count"])
        # stars = f":star: {stars}"
        issues = "{:,}".format(project["open_issues_count"])
        if args.forks:
            forks = project["forks"]
        project_time = project["updated_at"]
        # day = re.match(time, r"^[0-9]{4}-[0-9]{2}-[0-9]{2}")
        project_time = project_time[:10]
        project_time = dt.strptime(project_time, "%Y-%m-%d")

        if project_time.date() == dt.today().date():
            project_time = "Today"
        else:
            delta = dt.today().date() - project_time.date()
            if delta.days == 1:
                project_time = f"{str(delta.days)} day"
            else:
                project_time = f"{str(delta.days)} days"
        project_name = project['full_name']
        row = [
                project_name, project["description"],
                str(stars), str(issues), topics, project_time
            ]
        if args.forks:
            row.insert(4, str(forks))

        table_data.append(
            row
        )
    return table_data

def createTable(table):
    if(noColor):
        table.add_column("Project", header_style="bold", style="bold")
        table.add_column("Description", header_style="bold", style="italic")
        table.add_column("Stars", header_style="bold ")
        table.add_column("Issues", header_style="bold ")
        if args.forks:
            table.add_column("Forks", header_style="bold ")
        table.add_column("Tags", header_style="bold")
        table.add_column("Last updated", header_style="bold")
    else:
        table.add_column("Project", header_style="bold cyan", style="bold cyan")
        table.add_column("Description", header_style="bold green", style="italic green")
        table.add_column("Stars", header_style="bold yellow", style="yellow")
        table.add_column("Issues", header_style="bold grey66", style="grey66")
        if args.forks:
            table.add_column("Forks", header_style="bold dark_orange", style="dark_orange")
        table.add_column("Tags", header_style="bold")
        table.add_column("Last updated", header_style="red bold", style="red")


def display_table(table_data):
    table = Table(padding=(0, 1, 1, 1))
    createTable(table)
    table.add_row(*table_data[0])
    with Live(table, console=console, refresh_per_second=4):
        for row in table_data[1:]:
            table.add_row(*row)
            time.sleep(0.5)


def cli() -> None:
    print_welcome_message()
    url = get_url()
    console.clear()
    response = request(url)
    table_data = get_table_data(response)
    display_table(table_data)


if __name__ == "__main__":
    cli()
