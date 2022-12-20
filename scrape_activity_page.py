"""
Scrapes information from an activity page at activities.esn.org
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd

def get_activity_info(url):
    # Dictionary with page info
    activity_info = {}

    # Fetching page content
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Name
    name = list(soup.find("h1").stripped_strings)[0]
    activity_info["name"] = name

    # URL
    activity_info["url"] = url

    # Number of Participants
    participants = soup.find("div", {"class": "wrap-participants-text"}).div.div.text
    activity_info["participants"] = int(participants)

    # Organisers
    list_organisers = list(soup.find("div", {"class": "pseudo__items pseudo__organisers"}).stripped_strings)
    activity_info["organisers"] = list_organisers

    # Dates
    img_calendar = soup.find("img", # Should be on the same place no matter the event type and number of dates
        {"src": "/modules/custom/activities_core/images/icon_calendar_color.png"})
    list_dates = [datetime.strptime(x, "%d/%m/%Y") for x in img_calendar.parent.stripped_strings]
    activity_info["dates"] = list_dates

    # Causes
    list_causes = list(soup.find("div", {"class": "pseudo-field activity-causes"}).stripped_strings)
    activity_info["causes"] = list_causes

    # Objectives
    list_objectives = list(soup.find("div", {"class": "field__items activity__objectives"}).stripped_strings)
    activity_info["objectives"] = list_objectives

    # Goals
    img_goals = list(soup.find("div", text="By organising this activity, the organisers want to contribute to the "
                                           "following Sustainable Development Goals")
                     .parent.find_all("img", {"class": "sdg-logo-icon img-fluid"}))

    list_goals = [goal.get("title") for goal in img_goals]
    activity_info["goals"] = list_goals

    # Location of the event
    img_online = soup.find("img", {"src": "/modules/custom/activities_core/images/icon_portal_color.png"})
    img_physical = soup.find("img", {"src": "/modules/custom/activities_core/images/icon_location_color.png"})
    if img_online is not None:
        list_location = ["online"]
    elif img_physical is not None:
        list_location = list(img_physical.parent.stripped_strings)
    else:
        list_location = ""

    activity_info["location"] = list_location

    # Type of activity
    list_activity_type = list(soup.find("div", text=re.compile("Type of activity")).parent.stripped_strings)
    activity_info["types"] = list_activity_type[1:]

    return activity_info
