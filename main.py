from datetime import datetime
import pandas as pd
from pathlib import Path
from scrape_activity_page import get_activity_info
from scrape_activities_links import get_activities_links

FILE_NAME = Path(".", "data", "activities_summary.csv")

# Select a date range which is interesting for us
date_from = datetime(2022, 11, 29)
date_to = datetime(2022, 12, 28)

# Load links dataframe
df_links = get_activities_links(date_from, date_to)
links_count = df_links.shape[0]

# Go through all activities from selected date range to get necessary information

list_activities = []
print("\nDownloading the information from filtered activities...\n")

for index, url in enumerate(df_links.url):
    list_activities.append(get_activity_info(url))

    if index % max(int(links_count / 50), 1) == 0:
        print("\r", f"\t\tProgress: [{'=' * int(index / links_count * 49)}{'>'}"
                    f"{'.' * (49 - int(index / links_count * 49))}]", f"{index}/{links_count}", end="")

print("\n\nDownload complete.")
df_activities = pd.DataFrame(list_activities)

df_summary = df_activities[df_activities.columns[0]]
for col in df_activities.columns[1:]:
    df_split = pd.DataFrame(df_activities[col].tolist(),
                            columns=[f"{col}{i+1}" for i in range(pd.DataFrame(df_activities[col].tolist()).shape[1])])
    df_summary = pd.concat([df_summary, df_split], axis=1)

df_summary.to_csv(FILE_NAME)
# Analyze information about the activities
## Basic summary

## Counts
### NOs
### Sections
### Causes
### Goals
### Objectives
