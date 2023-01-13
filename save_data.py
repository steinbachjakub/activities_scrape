from datetime import datetime
import pandas as pd
from pathlib import Path
from scrape_activity_page import get_activity_info
from scrape_activities_links import get_activities_links

FILE_NAME_ACTIVITIES = Path(".", "data", "activities.csv")
FILE_NAME_ORGANISERS = Path(".", "data", "organisers.csv")
FILE_NAME_CAUSES = Path(".", "data", "causes.csv")
FILE_NAME_TYPES = Path(".", "data", "activity_type.csv")
FILE_NAME_GOALS = Path(".", "data", "goals.csv")
FILE_NAME_OBJECTIVES = Path(".", "data", "objectives.csv")

def save_activity_data(date_from, date_to):
    # Load links dataframe
    df_links = get_activities_links(date_from, date_to)
    links_count = df_links.shape[0]

    # Go through all activities from selected date range to get necessary information
    list_activities = []
    list_organisers = []
    list_causes = []
    list_activity_type = []
    list_goals = []
    list_objectives = []

    print("\nDownloading the information from filtered activities...\n")

    for index, url in enumerate(df_links.url):
        basic_info, organisers, causes, activity_types, goals, objectives = get_activity_info(url)

        df_activities_temp = pd.DataFrame(basic_info, index=[url])
        df_organisers_temp = pd.DataFrame({"organiser": organisers}, index=[url] * len(organisers))
        df_causes_temp = pd.DataFrame({"cause": causes}, index=[url] * len(causes))
        df_activity_type_temp = pd.DataFrame({"activity_type": activity_types}, index=[url] * len(activity_types))
        df_goals_temp = pd.DataFrame({"goal": goals}, index=[url] * len(goals))
        df_objectives_temp = pd.DataFrame({"objective": objectives}, index=[url] * len(objectives))

        list_activities.append(df_activities_temp)
        list_organisers.append(df_organisers_temp)
        list_causes.append(df_causes_temp)
        list_activity_type.append(df_activity_type_temp)
        list_goals.append(df_goals_temp)
        list_objectives.append(df_objectives_temp)

        if index % max(int(links_count / 50), 1) == 0:
            print("\r", f"\t\tProgress: [{'=' * int((index + 1) / links_count * 49)}{'>'}"
                        f"{'.' * (49 - int((index + 1) / links_count * 49))}]", f"{index}/{links_count}", end="")

    print("\n\nDownload complete.")

    df_activities = pd.concat(list_activities)
    df_organisers = pd.concat(list_organisers)
    df_causes = pd.concat(list_causes)
    df_activity_type = pd.concat(list_activity_type)
    df_goals = pd.concat(list_goals)
    df_objectives = pd.concat(list_objectives)

    # print(df_activities)
    # print(df_organisers)
    # print(df_causes)
    # print(df_activity_type)
    # print(df_goals)
    # print(df_objectives)


    df_activities.to_csv(FILE_NAME_ACTIVITIES)
    df_organisers.to_csv(FILE_NAME_ORGANISERS)
    df_causes.to_csv(FILE_NAME_CAUSES)
    df_activity_type.to_csv(FILE_NAME_TYPES)
    df_goals.to_csv(FILE_NAME_GOALS)
    df_objectives.to_csv(FILE_NAME_OBJECTIVES)

    return df_activities, df_organisers, df_causes, df_activity_type, df_goals, df_objectives
