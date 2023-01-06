from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager

# Paths to files
FILE_PATH_ACTIVITIES = Path("..", "data", "activities.csv")
FILE_PATH_ACTIVITY_TYPE = Path("..", "data", "activity_type.csv")
FILE_PATH_CAUSES = Path("..", "data", "causes.csv")
FILE_PATH_GOALS = Path("..", "data", "goals.csv")
FILE_PATH_OBJECTIVES = Path("..", "data", "objectives.csv")
FILE_PATH_ORGANISATIONS = Path("..", "data", "organisations.csv")
FILE_PATH_ORGANISERS = Path("..", "data", "organisers.csv")

OUTPUT_FOLDER = Path("..", "outputs")
IMAGE_FOLDER = Path("..", "images")

# ESN Colors
COLORS = {
    "darkblue": "#2E3192",
    "cyan": "#00AEEF",
    "magenta": "#EC008C",
    "green": "#7AC143",
    "orange": "#F47B20",
    "black": "#000000",
    "white": "#FFFFFF"
}

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
df_organisers_per_country = pd.merge(left=df_organisers.groupby("organiser").agg({"organiser": "count"}).rename(columns={"organiser": "count"}).reset_index(), right=df_organisations,
                                     how="outer", left_on="organiser", right_on="organisation_name")
df_organisers_per_country["country_name"] = df_organisers_per_country["country_name"].fillna("External Partner")
top_organiser_countries = df_organisers_per_country.groupby("country_name").agg(agg_func)\
    .rename(columns={"organiser": "count"}).sort_values("count", ascending=False)
# print(top_organiser_countries)
df_countries_org_number = df_organisations.groupby("country_name").agg({"country_name": "count"})\
      .rename(columns={"country_name": "total_count"})
df_countries_org_number["ratio"] = df_countries_org_number.join(top_organiser_countries)["count"] / \
                                   df_countries_org_number.join(top_organiser_countries)["total_count"]

top_organiser_countries.to_excel(OUTPUT_FOLDER.joinpath("top_organiser_countries.xlsx"))
df_countries_org_number.to_excel(OUTPUT_FOLDER.joinpath("top_organiser_countries_ratio.xlsx"))

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

# Visuals
plt.rcParams['font.family'] = 'Lato'
## Simple horizontal bar charts
data = [df_top_causes.sort_values("count")["count"],
        df_top_organisers.sort_values("count")["count"][-10:],
        df_countries_org_number.sort_values("ratio")["ratio"][-10:],
        top_organiser_countries[top_organiser_countries.index != "External Partner"].sort_values("count")["count"][-10:],
        df_top_types.sort_values("count")["count"][-10:],
        df_top_goals.sort_values("count")["count"][-10:],
        df_top_objectives.sort_values("count")["count"][-10:],
        df_participants_per_country.groupby("country_name").agg({"participants": "sum"}).sort_values("participants")["participants"][-10:]]

labels = [df_top_causes.sort_values("count").index,
          df_top_organisers.sort_values("count").index[-10:],
          df_countries_org_number.sort_values("ratio").index[-10:],
          top_organiser_countries[top_organiser_countries.index != "External Partner"].sort_values("count").index[-10:],
          df_top_types.sort_values("count").index[-10:],
          df_top_goals.sort_values("count").index[-10:],
          df_top_objectives.sort_values("count").index[-10:],
          df_participants_per_country.groupby("country_name").agg({"participants": "sum"}).sort_values("participants").index[-10:]]

titles = ["Number of Events\nDedicated to Each Cause",
          "Top 10 Organisers",
          "Top 10 Countries with\nthe Most Organisation Representation",
          "Top 10 Countries with\nthe Most Participating Organisations",
          "Top 10 Represented Types of Events",
          "Top 10 Reached Sustainable Development Goals",
          "Top 10 Reached Objectives",
          "Top 10 Countries by Number of Participants"]

styles = ["int", "int", "perc", "int", "int", "int", "int", "int"]
color = "darkblue"

# for color in COLORS.keys():
#     for i, (dataset, label, title, style) in enumerate(zip(data, labels, titles, styles)):
#         fig, ax = plt.subplots(1, 1, figsize=(16, 9))
#         bars = ax.barh(width=dataset, y=label,
#                        fc=COLORS[color])
#         ax.set_title(title, color=COLORS["black"], weight="bold", fontsize=25, va="center", font="Lato")
#         ax.set_yticklabels(label, fontsize=18, weight="bold", font="Lato")
#         ax.set_xticks([])
#         ax.tick_params(axis=u'both', which=u'both', length=0)
#         for bar in bars:
#           ax.text(
#               # df_top_causes.max() + 10,
#               0.01 * dataset.max(),
#               bar.get_y() + bar.get_height() / 2,
#               int(bar.get_width()) if style == "int" else f"{bar.get_width():.0%}",
#               ha="left",
#               va="center",
#               color=COLORS["white"],
#               weight='bold',
#               fontsize=18
#           )
#         for d in ["left", "top", "right", "bottom"]:
#             ax.spines[d].set_visible(False)
#
#         fig.patch.set_fc(COLORS[color])
#         fig.patch.set_alpha(0.2)
#         ax.patch.set_fc(COLORS[color])
#         ax.patch.set_alpha(0.00)
#         # plt.subplots_adjust(left=0.4, right=0.95, top=0.85, bottom=0.05)
#         plt.tight_layout()
#         fig.savefig(IMAGE_FOLDER.joinpath(f"{color}-fig{i}.png"))

## Pie Chart
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n({v:d})'.format(p=pct,v=val)
    return my_autopct
fig, ax = plt.subplots(1, 1, figsize=(9, 9))
_, _, autotexts = ax.pie(df_organisation_types["count"],
                         labels=["Local Sections", "External Partners", "National Organisations"],
                         textprops={'fontsize': 18, "weight": "bold"},
                         colors=[COLORS[key] for key in ["darkblue", "magenta", "green"]],
                         autopct=make_autopct(df_organisation_types["count"]),
                         wedgeprops={"edgecolor": COLORS["black"],
                                     'linewidth': 1,
                                     'antialiased': True}
                         )
ax.set_title("Participating Organisation Types", color=COLORS["black"], weight="bold", fontsize=25, va="center",
             font="Lato")
plt.tight_layout()

for autotext in autotexts:
    autotext.set_color(COLORS["white"])
    autotext.set_fontsize(18)
    autotext.set_fontweight("bold")

## Combined Horizontal Bar Chart
fig, ax = plt.subplots(1, 1, figsize=(16, 9))
ax2 = ax.twinx()
width = 0.4
df_countries_org_number["count"] = df_countries_org_number["total_count"] * df_countries_org_number["ratio"]
df_countries_org_number.sort_index()["count"].plot(kind='bar',
                                                                    color=COLORS["darkblue"],
                                                                    ax=ax,
                                                                    width=width,
                                                                    position=1)
df_countries_org_number.sort_index().ratio.plot(kind='bar',
                                                              color=COLORS["magenta"],
                                                              ax=ax2,
                                                              width=width,
                                                              position=0)
# print(df_countries_org_number.sort_values("ratio"))

plt.show()
