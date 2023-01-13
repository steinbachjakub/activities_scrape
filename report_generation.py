from matplotlib import pyplot as plt
from pathlib import Path
from docx import Document

from dev.functions.doc_style import change_styles
from dev.functions.chart_generation import generate_bar_chart, generate_map_chart
from dev.functions.chart_datasets import prepare_chart_datasets, prepare_map_datasets
from dev.functions.doc_sections_generation import generate_doc_intro, generate_doc_section, generate_doc_outro

GRAPH_TITLES_PATH = Path("dev", "files", "titles_graphs.txt")
GRAPH_TEXTS_PATH = Path("dev", "files", "texts_graphs.txt")
GRAPH_STYLE_PATH = Path("dev", "files", "style_graphs.mplstyle")

DOCUMENT_SAVE_PATH = Path("reports")
if not DOCUMENT_SAVE_PATH.exists():
    DOCUMENT_SAVE_PATH.mkdir()

def generate_doc_report(date_from, date_to):
    print("\n Generating document report...")
    # DATA
    # Preparing datasets and data
    chart_datasets = prepare_chart_datasets()
    causes, organisers, countries, types, goals, objectives, participants = chart_datasets
    map_datasets, gdf_countries = prepare_map_datasets()
    # Load titles
    with open(GRAPH_TITLES_PATH, "r") as f:
        titles = f.read().splitlines()
    # Document texts
    with open(GRAPH_TEXTS_PATH, "r") as f:
        texts = f.read().replace("\n", "")
    text_values = {
        "top_cause": causes.index[-1], "top_cause_count": causes['values'][-1],
        "top_section": organisers.index[-1], "top_section_count": organisers['values'][-1],
        "top_events_country": countries.index[-1],
        "top_type": types.index[-1], "top_type_count": types['values'][-1],
        "top_goal": goals.index[-1].split(': ')[1],
        "top_objective": objectives.index[-1],
        "top_country_participants": participants.index[-1], "top_country_participants_count": participants['values'][-1]
    }
    graph_texts = texts.format(**text_values).split("$")

    # GRAPH SETTINGS
    graph_colors = ["darkblue", "magenta", "cyan", "green", "orange"]
    plt.style.use(GRAPH_STYLE_PATH)
    # print(plt.rcParams.keys())

    # DOCUMENT SETTINGS
    # Generate document class
    document = Document()
    # Styles
    styles = change_styles(document.styles)
    title_style, header_style, text_style = styles

    # DOCUMENT GENERATION
    # Generating intro
    generate_doc_intro(document, styles, date_from, date_to)
    # Generating maps
    legend_titles = ["Number of submitted events", "Number of submitted participants"]
    for dataset, title in zip(map_datasets, legend_titles):
        generate_map_chart(dataset, title, date_from, date_to, gdf_countries)
        generate_doc_section(document, styles)
    # Generating graphs
    for i, (title, dataset, text) in enumerate(zip(titles, chart_datasets, graph_texts)):
        color = graph_colors[i % len(graph_colors)]
        generate_bar_chart(dataset, color)
        generate_doc_section(document, styles, text, title)
    # Generating the final word
    generate_doc_outro(document, styles)
    # Saving the document
    document.save(DOCUMENT_SAVE_PATH.joinpath(f'ESN Activities Report from {date_from} to {date_to}.docx'))
    # Deleting the temp file
    Path("fig_temp.png").unlink()