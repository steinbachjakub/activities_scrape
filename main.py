"""
Main script that collects the data and analyse them
"""

from datetime import datetime

from save_data import save_activity_data
from scrape_accounts import get_organisations

# Select a date range which is interesting for us
date_from = datetime(2022, 11, 7)
date_to = datetime(2022, 11, 20)

# Save data
dfs = save_activity_data(date_from, date_to)
df_activities, df_organisers, df_causes, df_activity_type, df_goals, df_objectives = dfs

# Import info on ESN Organisations
df_organisations = get_organisations()

