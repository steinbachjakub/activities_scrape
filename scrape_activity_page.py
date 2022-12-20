"""
Scrapes information from an activity page at activities.esn.org
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd

def get_activity_info(url):
    # Dictionary with basic information - wide format
    # URL, name, submitting organisation, number of organisers, number of participants, date from, date to,
    # location city, location country
    basic_info = {}

    # Fetching page content
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Name
    name = list(soup.find("h1").stripped_strings)[0]
    basic_info["name"] = name

    # Organisers
    list_organisers = list(soup.find("div", {"class": "pseudo__items pseudo__organisers"}).stripped_strings)
    basic_info["submitting_organiser"] = list_organisers[0]
    basic_info["num_of_organisers"] = len(list_organisers)

    # Number of Participants
    participants = soup.find("div", {"class": "wrap-participants-text"}).div.div.text
    basic_info["participants"] = int(participants)

    # Dates
    img_calendar = soup.find("img", # Should be on the same place no matter the event type and number of dates
        {"src": "/modules/custom/activities_core/images/icon_calendar_color.png"})
    list_dates = [datetime.strptime(x, "%d/%m/%Y") for x in img_calendar.parent.stripped_strings]
    if len(list_dates) == 2:
        basic_info["date_from"] = list_dates[0]
        basic_info["date_to"] = list_dates[1]
    else:
        basic_info["date_from"] = list_dates[0]
        basic_info["date_to"] = list_dates[0]

    # Causes
    list_causes = list(soup.find("div", {"class": "pseudo-field activity-causes"}).stripped_strings)

    # Objectives
    list_objectives = list(soup.find("div", {"class": "field__items activity__objectives"}).stripped_strings)

    # Goals
    img_goals = list(soup.find("div", text="By organising this activity, the organisers want to contribute to the "
                                           "following Sustainable Development Goals")
                     .parent.find_all("img", {"class": "sdg-logo-icon img-fluid"}))

    list_goals = [goal.get("title") for goal in img_goals]

    # Location of the event
    img_online = soup.find("img", {"src": "/modules/custom/activities_core/images/icon_portal_color.png"})
    img_physical = soup.find("img", {"src": "/modules/custom/activities_core/images/icon_location_color.png"})
    if img_online is not None:
        basic_info["location_city"] = "online"
        basic_info["location_country"] = ""
    elif img_physical is not None:
        basic_info["location_city"], basic_info["location_country"] = tuple(img_physical.parent.stripped_strings)

    # Type of activity
    list_activity_type = list(soup.find("div", text=re.compile("Type of activity")).parent.stripped_strings)[1:]

    return basic_info, list_organisers, list_causes, list_activity_type, list_goals, list_objectives
