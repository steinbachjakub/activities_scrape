from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

# ESN COLORS
COLORS = {
    "darkblue": "#2E3192",
    "cyan": "#00AEEF",
    "magenta": "#EC008C",
    "green": "#7AC143",
    "orange": "#F47B20",
    "black": "#000000",
    "white": "#FFFFFF",
    "grey": "#888888"
}

def generate_bar_chart(dataset, color):
    fig, ax = plt.subplots(figsize=(16, 9))
    labels = []
    for x in dataset.index:
        if len(x) > 30:
            labels.append(x[:x[:30].rfind(" ")] + "\n" + x[x[:30].rfind(" ") + 1:])
        else:
            labels.append(x)
    bars = ax.barh(width=dataset["values"], y=labels, alpha=0.98, facecolor=COLORS[color])
    for index, bar in enumerate(bars):
        ax.text(
            dataset["values"][index] - 0.1 * dataset.min(),
            bar.get_y() + bar.get_height() / 2,
            int(bar.get_width()),
            ha="right",
            va="center",
            color=COLORS["white"],
        )

    ax.set_axisbelow(True)
    ax.grid(which="major", axis="x", alpha=0.5)

    plt.tight_layout()
    plt.savefig("fig_temp.png")


def generate_map_chart(dataset, legend_title, date_from, date_to, gdf_countries):
    colors = gdf_countries.merge(dataset[["country_location", "values", "color"]], how="left",
                                           left_on="ADMIN", right_on="country_location")
    colors["color"] = colors["color"].cat.add_categories(["black", "grey"]).fillna(colors["base_color"])

    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    for c in colors["color"].unique():
        colors[colors["color"] == c].plot(ax=ax, color=COLORS[c], linewidth=0.1, ec="#CCCCCC")

    # Limits, clearing ticks
    ax.set_aspect(1.)
    ax.set_xlim(-15, 65)
    ax.set_ylim(30, 75)
    ax.set_xticks([])
    ax.set_yticks([])

    # Delete spines
    for d in ["left", "top", "right", "bottom"]:
        ax.spines[d].set_visible(False)

    # CUSTOM LEGEND
    # Calculating quartile borders
    borders = dataset["values"].quantile([0, 0.25, 0.5, 0.75, 1], interpolation="nearest").values
    borders[0] = 0
    # Creating labels
    legend_labels = ["no submission"]
    for i in range(len(borders) - 1):
        legend_labels.append(f"{int(borders[i] + 1):,} - {int(borders[i + 1]):,}")
    # Legend
    custom_lines = [Line2D([0], [0], color=COLORS["darkblue"], lw=4),
                    Line2D([0], [0], color=COLORS["cyan"], lw=4),
                    Line2D([0], [0], color=COLORS["orange"], lw=4),
                    Line2D([0], [0], color=COLORS["magenta"], lw=4),
                    Line2D([0], [0], color=COLORS["black"], lw=4)
                    ]

    ax.legend(custom_lines, legend_labels[-1::-1], title=f"{legend_title}\n{date_from} - {date_to}",
              loc="upper right")

    plt.tight_layout()
    plt.savefig("fig_temp.png")
