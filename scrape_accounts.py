"""
Searches for all sections and their National Organisations.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from pathlib import Path

def get_organisations():
    # Fetch the page with countries
    URL = "https://accounts.esn.org/"
    FILE_NAME = Path(".", "data", "organisations.csv")
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    # Save all country names and links to their pages
    a_countries = soup.find_all("a", {"href": re.compile("/country/")})
    countries = {
        "organisation_name": [x.text for x in a_countries],
        "organisation_link": [f"https://accounts.esn.org/{x.get('href')}" for x in a_countries],
        "country_name": [x.text for x in a_countries],
        "country_abbreviation": [x.get('href').split("/")[-1].upper() for x in a_countries],
        "type": ["national" for x in a_countries]
    }

    # Save all organisations under countries
    list_sections = []
    for country, link in zip(countries["country_name"], countries["organisation_link"]):
        response_country = requests.get(link)
        soup_country = BeautifulSoup(response_country.content, "html.parser")
        a_sections = soup_country.find_all("h2", {"class": "location-title", "property": "name"})
        sections = {
            "organisation_name": [x.text for x in a_sections],
            "organisation_link": [f"https://accounts.esn.org/{x.get('href')}" for x in a_sections],
            "country_name": [country for x in a_sections],
            "country_abbreviation": [link.split("/")[-1].upper() for x in a_sections],
            "type": ["local" for x in a_sections]
        }
        list_sections.append(sections)

    df_sections = pd.concat([pd.DataFrame(x) for x in list_sections])
    df_countries = pd.DataFrame(countries)
    df_organisations = pd.concat([df_sections, df_countries]).reset_index().drop("index", axis=1)
    df_organisations.to_csv(FILE_NAME)
    return df_organisations
