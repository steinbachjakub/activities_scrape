import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from pathlib import Path
from matplotlib.lines import Line2D

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

MAP_DATA_DIR = Path("map_data")
PATH_COUNTRIES = MAP_DATA_DIR.joinpath("countries.geojson")
PATH_ORGANISATIONS = Path("..", "data", "organisations.csv")
PATH_ACTIVITIES = Path("..", "data", "activities.csv")

df_organisations = pd.read_csv(PATH_ORGANISATIONS)
df_organisations["country_location"] = df_organisations["country_location"].replace("Czechia", "Czech Republic")
df_organisations["base_color"] = "black"
df_activities = pd.read_csv(PATH_ACTIVITIES)[["submitting_organiser", "participants"]]
df_events_org_country = df_activities.merge(df_organisations, how="left", left_on="submitting_organiser",
                                            right_on="organisation_name")
events_countries_count = df_events_org_country.groupby("country_location").agg({"country_location": "count"})\
    .rename(columns={"country_location": "event_count"}).reset_index()
events_countries_count["color"] = pd.qcut(events_countries_count["event_count"], q=[0, 0.25, 0.5, 0.75, 1],
                                          labels=["magenta", "orange", "cyan", "darkblue"])
gdf_countries = gpd.read_file(PATH_COUNTRIES)
gdf_countries["ADMIN"] = gdf_countries["ADMIN"].replace({
    "Cyprus No Mans Area": "Cyprus",
    "Northern Cyprus": "Cyprus",
    "Dhekelia Sovereign Base Area": "Cyprus",
    "Akrotiri Sovereign Base Area": "Cyprus",
    "Faroe Islands": "Denmark",
    "Aland": "Finland",
    "Republic of Serbia": "Serbia",
    "Bosnia and Herzegovina": "Bosnia & Herzegovina",
    "Isle of Man": "United Kingdom",
    "Jersey": "United Kingdom",
    "Guernsey": "United Kingdom"
})
gdf_countries = gdf_countries.merge(df_organisations[["country_location", "base_color"]], how="left", left_on="ADMIN",
                                    right_on="country_location").drop("country_location", axis=1)
gdf_countries["base_color"] = gdf_countries["base_color"].fillna("grey")

countries_colors = gdf_countries.merge(events_countries_count[["country_location", "color"]], how="left",
                                       left_on="ADMIN", right_on="country_location")
countries_colors["color"] = countries_colors["color"].cat.add_categories(["black", "grey"]).fillna(countries_colors["base_color"])
# print(countries_colors[["ADMIN", "color"]])
fig, ax = plt.subplots(1, 1, figsize=(16, 9))
for c in countries_colors["color"].unique():
    countries_colors[countries_colors["color"] == c].plot(ax=ax, color=COLORS[c], linewidth=0.1, ec="#CCCCCC")

# Limits, clearing ticks
ax.set_xlim(-15, 65)
ax.set_ylim(30, 75)
ax.set_xticks([])
ax.set_yticks([])

# Custom legend
# Calculating quartile borders
borders = events_countries_count["event_count"].quantile([0, 0.25, 0.5, 0.75, 1], interpolation="nearest").values
borders[0] = 0
# Creating labels
legend_labels = ["no submission"]
for i in range(len(borders) - 1):
    legend_labels.append(f"{borders[i] + 1} - {borders[i + 1]}")
# Legend
custom_lines = [Line2D([0], [0], color=COLORS["darkblue"], lw=4),
                Line2D([0], [0], color=COLORS["cyan"], lw=4),
                Line2D([0], [0], color=COLORS["orange"], lw=4),
                Line2D([0], [0], color=COLORS["magenta"], lw=4),
                Line2D([0], [0], color=COLORS["black"], lw=4)
                ]

ax.legend(custom_lines, legend_labels[-1::-1], title="Number of Submitted Events", loc="lower right")

print(events_countries_count)
plt.show()
