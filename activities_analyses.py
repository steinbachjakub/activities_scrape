import pandas as pd
from pathlib import Path

FILE_NAME = Path(".", "data", "activities.csv")
df_summary = pd.read_csv(FILE_NAME)

print(df_summary.columns)
print(df_summary[pd.notna(df_summary.objectives11)])
