from matplotlib import pyplot as plt
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Dates
DATE_FROM = "Nov 29, 2022"
DATE_TO = "Dec 28, 2022"

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

# Paths to files
FILE_PATH_ACTIVITIES = Path("data", "activities.csv")
FILE_PATH_ACTIVITY_TYPE = Path("data", "activity_type.csv")
FILE_PATH_CAUSES = Path("data", "causes.csv")
FILE_PATH_GOALS = Path("data", "goals.csv")
FILE_PATH_OBJECTIVES = Path("data", "objectives.csv")
FILE_PATH_ORGANISATIONS = Path("data", "organisations.csv")
FILE_PATH_ORGANISERS = Path("data", "organisers.csv")

# Loading data
df_activities = pd.read_csv(FILE_PATH_ACTIVITIES)
df_activity_type = pd.read_csv(FILE_PATH_ACTIVITY_TYPE)
df_causes = pd.read_csv(FILE_PATH_CAUSES)
df_goals = pd.read_csv(FILE_PATH_GOALS)
df_objectives = pd.read_csv(FILE_PATH_OBJECTIVES)
df_organisations = pd.read_csv(FILE_PATH_ORGANISATIONS)
df_organisers = pd.read_csv(FILE_PATH_ORGANISERS)

# General Font Specification
# plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Kelson Sans'
plt.rcParams['font.size'] = 25
# Figure Specification
plt.rcParams['figure.titlesize'] = 35
# Axes Specification
plt.rcParams['axes.labelpad'] = 10
plt.rcParams['axes.titlepad'] = 20
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['axes.spines.left'] = True
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 5
plt.rcParams['axes.edgecolor'] = "#666666"
# Grid Specification
plt.rcParams['grid.linewidth'] = 2.5
plt.rcParams['grid.linestyle'] = "-"
plt.rcParams['grid.color'] = "black"
# Y-tick Specification
plt.rcParams['ytick.left'] = False
plt.rcParams['ytick.major.pad'] = 20
plt.rcParams['ytick.labelsize'] = 25
# X-tick Specification
# plt.rcParams['xtick.major.pad'] = 20
# plt.rcParams['xtick.labelcolor'] = "white"
plt.rcParams['xtick.bottom'] = False
plt.rcParams['xtick.labelsize'] = 0

# print(plt.rcParams.keys())

# Analysing loaded data
causes = df_causes.groupby("cause").agg({"cause": "count"}).rename(columns={"cause": "values"}).sort_values("values")
organisers = df_organisers.groupby("organiser").agg({"organiser": "count"}).rename(columns={"organiser": "values"}).\
    sort_values("values")
organisers = organisers[organisers["values"] >= organisers["values"][-5]]
countries = df_organisers.merge(df_organisations[["organisation_name", "country_name"]], how="left",
                                left_on="organiser", right_on="organisation_name")\
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
# Preparing datasets and data
titles = ["Number of Events Dedicated to Each Cause",
          "Organisers with Top 5 Highest Organised Events",
          "ESN Countries with Top 5 Highest Organised Events",
          "Top 5 Represented Types of Events",
          "Top 5 Reached Sustainable Development Goals",
          "Top 5 Reached Objectives",
          "Countries with Top 5 Highest Number of Participants"]

datasets = [
    causes, organisers, countries, types, goals, objectives, participants
]

texts = [
    f"The most dedication goes to the {causes.index[-1]} cause with a total of {causes['values'][-1]} events being "
    f"dedicated to this cause. This is followed by the {causes.index[-2]} cause which was connected with {causes['values'][-2]} "
    f"events. Finally, the third cause most occuring during events is {causes.index[-3]} with the total of "
    f"{causes['values'][-3]} events. You can see the popularity of the remaining causes in the graph below.",
    f"{organisers.index[-1]} is on fire with whooping {organisers['values'][-1]} events organised in the "
    f"past month! Huge respect to you, friends!",
    f"Who's going to win, the David, or the Goliath? The first place to the country with the most organised events goes "
    f"to... {countries.index[-1]}!",
    f"What are your favorite types of events? We know ours, it's {types.index[-1]} with total of {types['values'][-1]} "
    f"dedicated events!",
    f"We all know how sustainable events are important! This month, we have dedicated our events mostly to "
    f"{goals.index[-1].split(': ')[1]}.",
    f"It's not all about fun! By organising events for our students, we have a perfect chance to educate our students "
    f"as well. This month, the objective number one was {objectives.index[-1]}.",
    f"Congratulations to {participants.index[-1]} for having the total of {participants['values'][-1]:,} participants "
    f"joining their events! You can see the other contenders with the top 5 highest total participants in the graph "
    f"below."
]

colors = ["darkblue", "magenta", "cyan", "green", "orange"]

# DOCUMENT
document = Document()
# STYLES
styles = document.styles
title_style = styles.add_style("TitleStyle", WD_STYLE_TYPE.PARAGRAPH)
title_style.font.name = "Kelson Sans"
title_style.font.size = Pt(24)
title_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
header_style = styles.add_style("HeaderStyle", WD_STYLE_TYPE.PARAGRAPH)
header_style.font.name = "Lato"
header_style.font.size = Pt(16)
header_style.font.bold = True
header_style.font.color.rgb = RGBColor(0x2E, 0x31, 0x92)
header_style.paragraph_format.keep_with_next = True
text_style = styles.add_style("TextStyle", WD_STYLE_TYPE.PARAGRAPH)
text_style.font.name = "Lato"
text_style.font.size = Pt(11)
text_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
text_style.paragraph_format.keep_with_next = True
text_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# WRITING THE DOCUMENT
document.add_paragraph('Monthly Activities Report', style=title_style)
document.add_paragraph(f'Dear network, this is the regular report of events submitted in ESN Activities. Below, you can find some higlights from the past month (for the period of {DATE_FROM} to {DATE_TO}).', style=text_style)
p = document.add_paragraph(style=text_style)
p.add_run("Are you curious about how your National Organisation or your local sections fare? Would you like us to create a similar report for you? No problem! Just contact us at ").bold = True
p.add_run("social-impact@esn.org").italic = True
p.add_run(".").bold = True
document.add_paragraph('Few Numbers First', style=header_style)
document.add_paragraph(f"In the past month, total of {df_activities.shape[0]:,} events were organised. The total of {df_activities['participants'].sum():,} participants joined our events which results in the average of {df_activities['participants'].mean():.2f} participants per one event.", style=text_style)

# GENERATING GRAPHS
for i, (title, dataset, text) in enumerate(zip(titles, datasets, texts)):
    document.add_paragraph(title.replace("\n", " "), style=header_style)
    document.add_paragraph(text, style=text_style)
    fig, ax = plt.subplots(figsize=(16, 9))
    labels = []
    for x in dataset.index:
        if len(x) > 30:
            labels.append(x[:x[:30].rfind(" ")] + "\n" + x[x[:30].rfind(" ") + 1:])
        else:
            labels.append(x)
    bars = ax.barh(width=dataset["values"], y=labels, alpha=0.98,
                   facecolor=COLORS[colors[i % len(colors)]])
    for index, bar in enumerate(bars):
        ax.text(
            dataset["values"][index] - 0.1 * dataset.min(),
            bar.get_y() + bar.get_height() / 2,
            int(bar.get_width()),
            ha="right",
            va="center",
            color=COLORS["white"],
        )
    # fig.suptitle(title, fontweight="bold")
    ax.set_axisbelow(True)
    ax.grid(which="major", axis="x", alpha=0.5)

    plt.tight_layout()
    plt.savefig("fig_temp.png")
    document.add_picture("fig_temp.png", height=Cm(8))
    document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if (i % 2 == 0) and (i < len(titles) - 1):
        document.add_page_break()

document.add_paragraph("That's all from us for now. See you next month!", style=text_style)
document.add_paragraph("Yours faithfully,\nSocial Impact Team", style=text_style)
document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.LEFT
document.save('demo.docx')

# plt.show()

# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True

# document.add_heading('Number of Events Dedicated to Each Cause', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')
#
# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )
#
# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )
#
# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc
#
# document.add_page_break()