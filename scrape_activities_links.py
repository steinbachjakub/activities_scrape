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
FILENAME = Path(".", "data", "activities_links.csv")

def get_activities_links(url=LINK, filename=FILENAME):

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
    current_page = 0
    while current_page <= 2:
        # Fetching page content for each page
        page_url = f"https://activities.esn.org/activities?page={current_page}"
        r = requests.get(page_url)
        soup = BeautifulSoup(r.content, "html.parser")

        # Fetching all information on articles on page
        list_articles = soup.find_all("article")

        # Iterating through articles to find the information
        for article in list_articles:
            name = list(article.find("div", {"class": re.compile("eg-c-card-title act-header")}).stripped_strings)[0]
            list_name.append(name)

            url = f'https://activities.esn.org{article.find("a", text=name).get("href")}'
            list_url.append(url)

            date = datetime.strptime(article.find("time").text, "%d/%m/%Y")
            list_date.append(date)

            location = list(article.find("span", {"class": "act-location-city"}).parent.stripped_strings)
            list_location.append([location])

            organiser = list(article.find("p", {"class": "act-organiser"}).stripped_strings)
            list_organiser.append(organiser)

        current_page += 1

        if current_page % int(last_page / 50) == 0:
            print("\r", f"Progress: [{'=' * int(current_page / last_page * 49)}{'>'}"
                  f"{'.' * (49 - int(current_page / last_page * 49))}]", f"{current_page}/{last_page}", end="")

    # Creating dataframe from scraped information for easier saving
    df = pd.DataFrame({
        "url": list_url,
        "name": list_name,
        "organiser": list_organiser,
        "location": list_location,
        "date": list_date
    })

    # Saving to file
    df.to_csv(FILENAME)
    print("Done")


