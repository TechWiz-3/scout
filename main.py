#!/usr/bin/env python3

import requests
import random
import os
import time

from contextlib import contextmanager

from rich.live import Live
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()

TOKEN = os.getenv("UNFOLLOW_TOKEN")

HEADERS = {'Authorization': 'token ' + TOKEN}

BASE_URL = "https://api.github.com/search/repositories?q=stars:%3E={}%20language:{}%20topic:hacktoberfest"


def get_url():
    #lang = input("Language: ")
    #min_stars = int(input("Minimum stars: "))
    lang = "python"
    min_stars = 20
    url = BASE_URL.format(min_stars, lang)
    return url

def request(url):
    response = requests.get(f"{url}&page=1", headers=HEADERS)
    response = response.json()
    return response


def get_table_data(response: str) -> list:
    table_data = []
    for project in random.sample(response["items"],min(5, 29)):
        topics = "` `".join(project["topics"])
        topics = f"`{topics}`"
        topics = Markdown(topics, style="dim")
        stars = "{:,}".format(project["stargazers_count"])
        table_data.append(
                    [
                        project["name"], project["description"],
                        str(stars), topics, "time"
                    ]
                )
    return table_data


def display_table(table_data):
    table = Table(padding=(0,1,1,1))
    table.add_column("Project")
    table.add_column("Description")
    table.add_column("Stars")
    table.add_column("Tags")
    table.add_column("Last updated")
    table.add_row(*table_data[0])
    with Live(table, console=console, refresh_per_second=4):
        for row in table_data[1:]:
            table.add_row(*row)
            time.sleep(0.5)


console.clear()
url = get_url()
response = request(url)
table_data = get_table_data(response)
display_table(table_data)
