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
    print(url)
    return url

def request(url):
    response = requests.get(f"{url}&page=1", headers=HEADERS)
    response = response.json()
    return response

BEAT_TIME = 0.04

@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * BEAT_TIME)


def get_table(response, add_row_only=False) -> Table:
    global table
    if add_row_only:
        projects = random.sample(response["items"],min(1, 29))
        project = projects[0]
        topics = "` `".join(project["topics"])
        topics = f"`{topics}`"
        topics = Markdown(topics, style="dim")
        stars = "{:,}".format(project["stargazers_count"])
        table.add_row(project["name"], project["description"],
                        str(stars),
                        topics, "time")
    else:
        table = Table(padding=(0,1,1,1))
        table.add_column("Project")
        table.add_column("Description")
        table.add_column("Stars")
        table.add_column("Tags")
        table.add_column("Last updated")
        projects = random.sample(response["items"],min(1, 29))
        project = projects[0]
        topics = "` `".join(project["topics"])
        topics = f"`{topics}`"
        topics = Markdown(topics, style="dim")
        stars = "{:,}".format(project["stargazers_count"])
        table.add_row(project["name"], project["description"],
                        str(stars),
                        topics, "time")
    return table


def display_table():
    global response
    with Live(get_table(response), console=console, refresh_per_second=4) as live:
        for i in range(4):
            time.sleep(0.4)
            live.update(get_table(response, add_row_only=True))
#        console.print(table)


url = get_url()
response = request(url)
console.clear()
rendered_table = get_table(response)
display_table()
