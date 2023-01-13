"""
Searches through all activities pages at activities.esn.org and returns a list of all activitties with their URL, name,
organiser and other information.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
from pathlib import Path

LINK = "https://activities.esn.org/activities"
DATA_PATH = Path(".", "data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir()


def get_activities_links(date_from, date_to, url=LINK, path=DATA_PATH):

    # Fetching page content
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Fetching the last page number
    last_page = int(soup.find("a", {"title": "Go to last page"}).get("href").split("page=")[-1])

    # Creating separate lists for each provided information
    list_name = []
    list_url = []
    list_date = []
    list_location = []
    list_organiser = []

    # Iterating through all pages
    print("\nChecking Activities for events in the desired range...\n")
    current_page = 0
    count = 0
    while current_page <= last_page:
        # Fetching page content for each page
        page_url = f"https://activities.esn.org/activities?page={current_page}"
        r = requests.get(page_url)
        soup = BeautifulSoup(r.content, "html.parser")

        # Checking date_to
        dates = [datetime.strptime(x.text, "%d/%m/%Y") for x in soup.find_all("time")]

        if min(dates) > date_to:
            current_page += 1
            continue
        elif max(dates) < date_from:
            break

        if count % 5 == 0:
            print(f"\r"
                  f"\t\tChecking page {current_page}, the latest date {datetime.strftime(max(dates), '%d/%m/%Y')} is "
                  f"within the range of {datetime.strftime(date_from, '%d/%m/%Y')} - "
                  f"{datetime.strftime(date_to, '%d/%m/%Y')}.", end="")
        count += 1

        # Fetching all information on articles on page
        list_articles = soup.find_all("article")

        # Iterating through articles to find the information
        for article in list_articles:
            name = list(article.find("div", {"class": re.compile("eg-c-card-title act-header")}).stripped_strings)[0]
            list_name.append(name)
            url = f'https://activities.esn.org{article.find("div", {"class": re.compile("eg-c-card-title act-header")}).find("a", {"href": re.compile("/activity/")}).get("href")}'
            list_url.append(url)

            date = [datetime.strptime(x.text, "%d/%m/%Y") for x in article.find_all("time")]
            list_date.append(date)

            location = list(article.find("span", {"class": "act-location-city"}).parent.stripped_strings)
            list_location.append(location)

            organiser = list(article.find("p", {"class": "act-organiser"}).stripped_strings)
            list_organiser.append(organiser)

        current_page += 1

    # Creating dataframe from scraped information for easier saving
    df = pd.DataFrame({
        "url": list_url,
        "name": list_name,
        "organiser": list_organiser,
        "location": list_location,
        "date": list_date
    })

    # Splitting dates to be able to compare them with limits
    df_date_split = pd.DataFrame(df["date"].tolist())
    # Filtering events based on the dates - either starting or ending date needs to be in the specified range
    df_filtered = df[(df_date_split.max(axis=1) >= date_from) &
                     (df_date_split.min(axis=1) <= date_to)]

    # Saving to file
    df_filtered.to_csv(path.joinpath("activities_links.csv"))
    print("\n\nLinks to filtered activitites saved.")
    return df_filtered


