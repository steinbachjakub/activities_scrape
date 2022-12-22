from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt

# Paths to files
FILE_PATH_ACTIVITIES = Path(".", "data", "activities.csv")
FILE_PATH_ACTIVITY_TYPE = Path(".", "data", "activity_type.csv")
FILE_PATH_CAUSES = Path(".", "data", "causes.csv")
FILE_PATH_GOALS = Path(".", "data", "goals.csv")
FILE_PATH_OBJECTIVES = Path(".", "data", "objectives.csv")
FILE_PATH_ORGANISATIONS = Path(".", "data", "organisations.csv")
FILE_PATH_ORGANISERS = Path(".", "data", "organisers.csv")

OUTPUT_FOLDER = Path(".", "outputs")

# Loading data
df_activities = pd.read_csv(FILE_PATH_ACTIVITIES)
df_activity_type = pd.read_csv(FILE_PATH_ACTIVITY_TYPE)
df_causes = pd.read_csv(FILE_PATH_CAUSES)
df_goals = pd.read_csv(FILE_PATH_GOALS)
df_objectives = pd.read_csv(FILE_PATH_OBJECTIVES)
df_organisations = pd.read_csv(FILE_PATH_ORGANISATIONS)
df_organisers = pd.read_csv(FILE_PATH_ORGANISERS)

# Overview of activities
df_activities.to_excel(OUTPUT_FOLDER.joinpath("activities_summary.xlsx"))

# Organisers
## Top Organisers
# print("Number of organised events per organisation")
df_top_organisers = df_organisers.groupby("organiser").agg({"organiser": "count"})\
    .rename(columns={"organiser": "count"}).sort_values("count", ascending=False)
# print(df_top_organisers)
df_top_organisers.to_excel(OUTPUT_FOLDER.joinpath("top_organisers.xlsx"))

## Number of organisers per country
# print("\n\nNumber of organisations involved in event preparation per country")
agg_func = {'organiser': 'count'}
df_organisers_per_country = pd.merge(left=df_organisers, right=df_organisations,
                                     how="outer", left_on="organiser", right_on="organisation_name")
df_organisers_per_country["country_name"] = df_organisers_per_country["country_name"].fillna("External Partner")
top_organiser_countries = df_organisers_per_country.groupby("country_name").agg(agg_func)\
    .rename(columns={"organiser": "count"}).sort_values("count", ascending=False)
# print(top_organiser_countries)
top_organiser_countries.to_excel(OUTPUT_FOLDER.joinpath("top_organiser_countries.xlsx"))

## Ratio of sections organising at least one event
df_country_ratio = pd.merge(left=df_organisers.drop_duplicates("organiser"),
                                           right=df_organisations[df_organisations.type == "local"],
                                           how="right", left_on="organiser", right_on="organisation_name")
df_country_ratio["organised_event"] = df_country_ratio["organiser"] == df_country_ratio["organisation_name"]
df_country_ratio = df_country_ratio[["country_name", "organised_event"]]
# print(df_country_ratio.groupby(["country_name", "organised_event"]).agg({"country_name": "count"}))
## Number of local versus national versus external organisers
# print("\n\nNumber of local versus national versus external organisations involved in event preparation")
df_organisers_per_country["type"] = df_organisers_per_country["type"].fillna("External Partner")
df_organisation_types = df_organisers_per_country.groupby("type").agg(agg_func).rename(columns={"organiser": "count"})\
      .sort_values("count", ascending=False)
# print(df_organisation_types)
df_organisation_types.to_excel(OUTPUT_FOLDER.joinpath("organisation_types.xlsx"))

## Number of participants per country based on the submitting section
df_participants_per_country = pd.merge(left=df_activities, right=df_organisations,
                                       how="right", left_on="submitting_organiser", right_on="organisation_name")
# print("\n\nNumber of participants per country based on the submitting section")
df_participants = df_participants_per_country.groupby("country_name").agg({"participants": "sum"})\
    .rename(columns={"participants": "total"}).sort_values("total", ascending=False)
# print(df_participants)
df_participants.to_excel(OUTPUT_FOLDER.joinpath("participants.xlsx"))

# Causes
## Number of events per cause
# print("\n\nNumber of events per cause")
df_top_causes = df_causes.groupby("cause").agg({"cause": "count"}).rename(columns={"cause": "count"})\
      .sort_values("count", ascending=False)
# print(df_top_causes)
df_top_causes.to_excel(OUTPUT_FOLDER.joinpath("top_causes.xlsx"))

# Activity types
## Number of events per type
# print("\n\nNumber of events per type")
df_top_types = df_activity_type.groupby("activity_type").agg({"activity_type": "count"})\
    .rename(columns={"activity_type": "count"}).sort_values("count", ascending=False)
# print(df_top_types)
df_top_types.to_excel(OUTPUT_FOLDER.joinpath("top_types.xlsx"))

# Objectives
## Number of events per objective
# print("\n\nNumber of events per objective")
df_top_objectives = df_objectives.groupby("objective").agg({"objective": "count"})\
    .rename(columns={"objective": "count"}).sort_values("count", ascending=False)
# print(df_top_objectives)
df_top_objectives.to_excel(OUTPUT_FOLDER.joinpath("top_objectives.xlsx"))

# Sustainable Development Goals
## Number of events per SDG
# print("\n\nNumber of events per SDG")
df_top_goals = df_goals.groupby("goal").agg({"goal": "count"}).rename(columns={"goal": "count"})\
      .sort_values("count", ascending=False)
# print(df_top_goals)
df_top_goals.to_excel(OUTPUT_FOLDER.joinpath("top_goals.xlsx"))
