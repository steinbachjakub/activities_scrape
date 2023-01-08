import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
from matplotlib.lines import Line2D

# Dates
DATE_FROM = "Nov 29, 2022"
DATE_TO = "Dec 28, 2022"

# ESN Colors
COLORS = {
    "darkblue": "#2E3192",
    "cyan": "#00AEEF",
    "magenta": "#EC008C",
    "green": "#7AC143",
    "orange": "#F47B20",
    "black": "#000000",
    "white": "#FFFFFF",
    "grey": "#888888"
}

# FILE PATHS
MAP_DATA_DIR = Path("map_data")
PATH_COUNTRIES = MAP_DATA_DIR.joinpath("countries.geojson")
PATH_ORGANISATIONS = Path("..", "data", "organisations.csv")
PATH_ACTIVITIES = Path("..", "data", "activities.csv")

# MAP PREPARATION
df_organisations = pd.read_csv(PATH_ORGANISATIONS)
df_organisations["base_color"] = "black"
gdf_countries = gpd.read_file(PATH_COUNTRIES)
gdf_countries = gdf_countries.merge(df_organisations[["country_location", "base_color"]], how="left", left_on="ADMIN",
                                    right_on="country_location").drop("country_location", axis=1)
gdf_countries["base_color"] = gdf_countries["base_color"].fillna("grey")

# MAP GENERATION FUNCTION
def generate_map(dataset, legend_title, date_from, date_to):
    colors = gdf_countries.merge(dataset[["country_location", "values", "color"]], how="left",
                                           left_on="ADMIN", right_on="country_location")
    colors["color"] = colors["color"].cat.add_categories(["black", "grey"]).fillna(colors["base_color"])

    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    for c in colors["color"].unique():
        colors[colors["color"] == c].plot(ax=ax, color=COLORS[c], linewidth=0.1, ec="#CCCCCC")

    # Limits, clearing ticks
    ax.set_aspect(1.)
    ax.set_xlim(-15, 65)
    ax.set_ylim(30, 75)
    ax.set_xticks([])
    ax.set_yticks([])

    # CUSTOM LEGEND
    # Calculating quartile borders
    borders = dataset["values"].quantile([0, 0.25, 0.5, 0.75, 1], interpolation="nearest").values
    borders[0] = 0
    # Creating labels
    legend_labels = ["no submission"]
    for i in range(len(borders) - 1):
        legend_labels.append(f"{int(borders[i] + 1):,} - {int(borders[i + 1]):,}")
    # Legend
    custom_lines = [Line2D([0], [0], color=COLORS["darkblue"], lw=4),
                    Line2D([0], [0], color=COLORS["cyan"], lw=4),
                    Line2D([0], [0], color=COLORS["orange"], lw=4),
                    Line2D([0], [0], color=COLORS["magenta"], lw=4),
                    Line2D([0], [0], color=COLORS["black"], lw=4)
                    ]

    ax.legend(custom_lines, legend_labels[-1::-1], title=f"{legend_title}\n{date_from} - {date_to}",
              loc="lower right")

# DATA ANALYSIS
df_activities = pd.read_csv(PATH_ACTIVITIES)[["submitting_organiser", "participants"]]
df_events_org_country = df_activities.merge(df_organisations, how="left", left_on="submitting_organiser",
                                            right_on="organisation_name")
events_countries_count = df_events_org_country.groupby("country_location").agg({"country_location": "count"})\
    .rename(columns={"country_location": "values"}).reset_index()
events_countries_count["color"] = pd.qcut(events_countries_count["values"], q=4,
                                          labels=["magenta", "orange", "cyan", "darkblue"])

participants_countries_count = df_events_org_country.groupby("country_location").agg({"participants": "sum"})\
    .rename(columns={"participants": "values"}).reset_index()
participants_countries_count["color"] = pd.qcut(participants_countries_count["values"], q=4,
                                          labels=["magenta", "orange", "cyan", "darkblue"])

# MAP PLOT
datasets = [events_countries_count, participants_countries_count]
legend_titles = ["Number of submitted events", "Number of submitted participants"]
for dataset, legend_title in zip(datasets, legend_titles):
    generate_map(dataset, legend_title, DATE_FROM, DATE_TO)

    plt.tight_layout()
plt.show()
