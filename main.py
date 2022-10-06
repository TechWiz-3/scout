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

def table(response):
    first = True
    table = Table(padding=(0,1,1,1))
    table.add_column("Project")
    table.add_column("Description")
    table.add_column("Stars")
    table.add_column("Tags")
    table.add_column("Last updated")
    with Live(table, console=console, refresh_per_second=1):
        for project in random.sample(response["items"],min(5, 29)):
            topics = "` `".join(project["topics"])
            topics = f"`{topics}`"
            topics = Markdown(topics, style="dim")
            stars = "{:,}".format(project["stargazers_count"])
            if not first:
                with beat(10):
                    table.add_row(project["name"], project["description"],
                                  str(stars),
                                  topics, "time")
            else:
                table.add_row(project["name"], project["description"],
                    str(stars),
                    topics, "time")

            first = False
#        console.print(table)


url = get_url()
response = request(url)
console.clear()
table(response)
