"""
Main script that collects the data and analyse them
"""

from datetime import datetime

from save_data import save_activity_data
from scrape_accounts import get_organisations
from report_generation import generate_doc_report

# Select a date range which is interesting for us
date_from = datetime(2022, 11, 29)
date_to = datetime(2022, 12, 28)

# Save data
dfs = save_activity_data(date_from, date_to)
df_activities, df_organisers, df_causes, df_activity_type, df_goals, df_objectives = dfs

# Import info on ESN Organisations
df_organisations = get_organisations()

# Generate document report
date_from_text = date_from.strftime("%b %d, %Y")
date_to_text = date_to.strftime("%b %d, %Y")
generate_doc_report(date_from_text, date_to_text)

