from scrape_activity_page import get_activity_info
from scrape_activities_links import get_activities_links

# Get all links from activities
get_activities_links()

# Select a date range which is interesting for us

# Go through all activities from selected date range to get necessary information
print(get_activity_info("https://activities.esn.org/activity/international-day-people-disabilities-post-and-qa-11530"))

# Analyze information about the activities
## Organisers

## Causes

## Online vs. offline