from pathlib import Path
import pandas as pd
import geopandas as gpd

# FILE PATHS
FILE_PATH_ACTIVITIES = Path(".", ".", ".", "data", "activities.csv")
FILE_PATH_ACTIVITY_TYPE = Path(".", ".", ".", "data", "activity_type.csv")
FILE_PATH_CAUSES = Path(".", ".", ".", "data", "causes.csv")
FILE_PATH_GOALS = Path(".", ".", ".", "data", "goals.csv")
FILE_PATH_OBJECTIVES = Path(".", ".", ".", "data", "objectives.csv")
FILE_PATH_ORGANISATIONS = Path(".", ".", ".", "data", "organisations.csv")
FILE_PATH_ORGANISERS = Path(".", ".", ".", "data", "organisers.csv")
PATH_COUNTRIES = Path("dev", "files", "countries.geojson")

# LOADING SCRAPED DATA
df_activities = pd.read_csv(FILE_PATH_ACTIVITIES)
df_activity_type = pd.read_csv(FILE_PATH_ACTIVITY_TYPE)
df_causes = pd.read_csv(FILE_PATH_CAUSES)
df_goals = pd.read_csv(FILE_PATH_GOALS)
df_objectives = pd.read_csv(FILE_PATH_OBJECTIVES)
df_organisations = pd.read_csv(FILE_PATH_ORGANISATIONS)
df_organisers = pd.read_csv(FILE_PATH_ORGANISERS)

# LOADING COUNTRY MAP DATA
df_organisations["base_color"] = "black"
gdf_countries = gpd.read_file(PATH_COUNTRIES)
gdf_countries = gdf_countries.merge(df_organisations[["country_location", "base_color"]], how="left", left_on="ADMIN",
                                    right_on="country_location").drop("country_location", axis=1)
gdf_countries["base_color"] = gdf_countries["base_color"].fillna("grey")


def prepare_chart_datasets():
    # Analysing loaded data
    causes = df_causes.groupby("cause").agg({"cause": "count"}).rename(columns={"cause": "values"})\
        .sort_values("values")
    organisers = df_organisers.groupby("organiser").agg({"organiser": "count"})\
        .rename(columns={"organiser": "values"}).sort_values("values")
    organisers = organisers[organisers["values"] >= organisers["values"][-5]]
    countries = df_activities[["submitting_organiser"]].merge(df_organisations[["organisation_name", "country_name"]],
                                                              how="left", left_on="submitting_organiser",
                                                              right_on="organisation_name")\
        .groupby("country_name").agg({"country_name": "count"}).rename(columns={"country_name": "values"})\
        .sort_values("values")
    countries = countries[countries["values"] >= countries["values"][-5]]
    types = df_activity_type.groupby("activity_type").agg({"activity_type": "count"})\
        .rename(columns={"activity_type": "values"}).sort_values("values")[-5:]
    goals = df_goals.groupby("goal").agg({"goal": "count"}).rename(columns={"goal": "values"})\
        .sort_values("values")[-5:]
    objectives = df_objectives.groupby("objective").agg({"objective": "count"}).rename(columns={"objective": "values"})\
        .sort_values("values")[-5:]
    participants = df_activities[["submitting_organiser", "participants"]]\
        .merge(df_organisations[["organisation_name", "country_name"]], how="left",
               left_on="submitting_organiser", right_on="organisation_name").groupby("country_name")\
        .agg({"participants": "sum"}).rename(columns={"participants": "values"}).sort_values("values")
    participants = participants[participants["values"] >= participants["values"][-5]]

    return causes, organisers, countries, types, goals, objectives, participants


def prepare_map_datasets():
    df_events_org_country = df_activities[["submitting_organiser", "participants"]]\
        .merge(df_organisations, how="left", left_on="submitting_organiser", right_on="organisation_name")
    events_countries_count = df_events_org_country.groupby("country_location").agg({"country_location": "count"}) \
        .rename(columns={"country_location": "values"}).reset_index()
    events_countries_count["color"] = pd.qcut(events_countries_count["values"], q=4,
                                              labels=["magenta", "orange", "cyan", "darkblue"])

    participants_countries_count = df_events_org_country.groupby("country_location").agg({"participants": "sum"}) \
        .rename(columns={"participants": "values"}).reset_index()
    participants_countries_count["color"] = pd.qcut(participants_countries_count["values"], q=4,
                                                    labels=["magenta", "orange", "cyan", "darkblue"])

    return (events_countries_count, participants_countries_count), gdf_countries
