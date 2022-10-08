#!/usr/bin/env python3
import argparse
from unicodedata import name
import requests
import random
import os
import time
import re
import sys
from datetime import datetime as dt

from contextlib import contextmanager

from rich.live import Live
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from rich.markdown import Markdown

console = Console()

TOKEN = os.getenv("SCOUT_TOKEN")

HEADERS = {'Authorization': 'token ' + TOKEN}

# BASE_URL = "https://api.github.com/search/repositories?q=stars:%3E={}%20language:{}%20topic:hacktoberfest"
BASE_URL = "https://api.github.com/search/repositories?q={}stars:%3C={}%20language:{}%20topic:hacktoberfest"

#global variable
noColor = False

#theme dict
theme = {
    "standard":{
        "color":"[purple]Shall I use the standard search which gets repos in the 1k stars range? \[y/n]: ", 
        "nocolor":"Shall I use the standard search which gets repos in the 1k stars range? \[y/n]: "
        },
    "lang":{
        "color":"Project language: \[python] ",
        "nocolor":"Project language: \[python] "
        },
    "keyword":{
        "color":"[purple]You can enter a keyword for the search: \[optional] ",
        "nocolor":"You can enter a keyword for the search: \[optional] "
        },
    "max_star":{
        "color":"[blue]Star count  range \[5-1000 is ideal]: ",
        "nocolor":"Star count  range \[5-1000 is ideal]: " 
        },
    "rule":{
        "color":{
            "value":"[b]Your personal opensource [purple]Scout",
            "align":"center",
            "style":"yellow",
        },
        "nocolor":{
            "value":"[b]Your personal opensource [purple]Scout",
            "align":"center",
            "style":"",
        }
        }
}
# table theme dic
tableTheme={
    "Project":{
        "color":{
            "name":"Project",
            "headerStyle":"bold cyan",
            "style":"bold cyan"
        },
        "nocolor":{
            "name":"Project",
            "headerStyle":"bold",
            "style":"bold"
        }
        },
    "Description":{
        "color":{
            "name":"Description",
            "headerStyle":"bold green",
            "style":"bold green"
        },
        "nocolor":{
            "name":"Description",
            "headerStyle":"bold",
            "style":"italic"
        }
        },
    "Stars":{
        "color":{
            "name":"Stars",
            "headerStyle":"bold yellow",
            "style":"bold yellow"
            },
        "nocolor":{
            "name":"Stars",
            "headerStyle":"bold",
            "style":""
        }
        },
    "Issues":{
        "color":{
            "name":"Issues",
            "headerStyle":"bold grey66",
            "style":"grey66"
            },
        "nocolor":{
            "name":"Issues",
            "headerStyle":"bold",
            "style":""
        }
        },
    "Tags":{
        "color":{
            "name":"Tags",
            "headerStyle":"bold",
        },
        "nocolor":{
            "name":"Tags",
            "headerStyle":"bold",
        }
        },
    "Last-updated":{
        "color":{
            "name":"Last updated",
            "headerStyle":"red bold",
            "style":"red"
        },
        "nocolor":{
            "name":"Last updated",
            "headerStyle":"bold",
            "style":""
        }
        },
}

# theme setter based on script args --nocolor
def themeSetter():
    if noColor: 
        themeColor = "nocolor"
    else: 
        themeColor = "color"
    return themeColor


def print_welcome_message() -> None:
    themeColor = themeSetter()
    ruleTheme = theme.get("rule").get(themeColor)
    rule = Rule(ruleTheme.get("value"),align=ruleTheme.get("align"),style=ruleTheme.get("style"))
    console.print(rule)
    print("")



def get_url():
    # getting theme color or no color
    themeColor = themeSetter()
    try:
        standard = console.input(theme.get("standard").get(themeColor))
        
        # standard = console.input("[purple]Shall I use the standard search which gets repos in the 1k stars range? \[y/n]: ")
        # lang = console.input("Project language: \[python] ")
        lang = console.input(theme.get("lang").get(themeColor))
        # keyword = console.input("[purple]You can enter a keyword for the search: \[optional] ")
        keyword = console.input(theme.get("keyword").get(themeColor))

    except KeyboardInterrupt:
        print('\nFarewell my friend, beware the crickets.\n')
        sys.exit(1)

    else:
        if standard.lower() in ("y", "yes", ""):
            max_stars = 1000
        else:
            # max_stars = int(console.input("[blue]Star count  range \[5-1000 is ideal]: "))
            max_stars = int(console.input(theme.get("max_star").get(themeColor)))

        if lang == "":
            lang = "python"

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
                        "[link={}]{}[/link]".format(project["html_url"], project["full_name"]), project["description"],
                        str(stars), str(issues), topics, time
                    ]
                )
    return table_data

def display_table(table_data):
    # getting theme color or nocolor
    themeColor = themeSetter()
    table = Table(padding=(0,1,1,1))
    
    # table theme 
    project = tableTheme.get("Project").get(themeColor)
    description = tableTheme.get("Description").get(themeColor)
    stars = tableTheme.get("Stars").get(themeColor)
    issues = tableTheme.get("Issues").get(themeColor)
    tags = tableTheme.get("Tags").get(themeColor)
    lastUpdate = tableTheme.get("Last-updated").get(themeColor)
    
    # table column
    table.add_column(project.get("name"), header_style=project.get("headerStyle"), style=project.get("style"))
    table.add_column(description.get("name"), header_style=description.get("headerStyle"), style=description.get("style"))
    table.add_column(stars.get("name"), header_style=stars.get("headerStyle"), style=stars.get("style"))
    table.add_column(issues.get("name"), header_style=issues.get("headerStyle"), style=issues.get("style"))
    table.add_column(tags.get("name"), header_style=tags.get("headerStyle"))
    table.add_column(lastUpdate.get("name"), header_style=lastUpdate.get("headerStyle"), style=lastUpdate.get("style"))
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--nocolor", help="color theme default ",action="store_true")
    args = parser.parse_args()
    noColor = args.nocolor
    cli()
