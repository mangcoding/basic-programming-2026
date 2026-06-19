#!/usr/bin/env python3
"""
Quiz score distribution infographic by score group.

Reads data from score-quiz.xlsx and displays a visualization using matplotlib.
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Score group configuration: (label, lower_bound, upper_bound)
# lower_bound is inclusive, upper_bound is inclusive
SCORE_GROUPS = [
    ("0 - 50", 0, 50),
    ("50 - 70", 50, 70),
    ("70 - 80", 70, 80),
    ("80 - 90", 80, 90),
    ("> 90", 90, 100),
]

COLORS = ["#E74C3C", "#F39C12", "#3498DB", "#2ECC71", "#9B59B6"]

SCORE_COLUMN_CANDIDATES = ["Total Score (norm.)", "Total Skor (norm.)"]


def get_score_column(df):
    """Return the normalized total score column from the quiz export."""
    for column in SCORE_COLUMN_CANDIDATES:
        if column in df.columns:
            return column
    raise KeyError(
        "Score column not found. Expected one of: "
        + ", ".join(SCORE_COLUMN_CANDIDATES)
    )


def parse_score(value):
    """Extract the score value from the 'Total Score (norm.)' column, e.g. '95.3 (90%)'."""
    if pd.isna(value):
        return None
    match = re.match(r"^([\d.]+)", str(value).strip())
    return float(match.group(1)) if match else None


def categorize_score(score):
    """Assign a score to the appropriate score group."""
    if score <= 50:
        return "0 - 50"
    if score <= 70:
        return "50 - 70"
    if score < 80:
        return "70 - 80"
    if score <= 90:
        return "80 - 90"
    return "> 90"


def count_per_group(score_list):
    """Count the number of participants in each score group."""
    group_labels = [g[0] for g in SCORE_GROUPS]
    counts = {label: 0 for label in group_labels}

    for score in score_list:
        group = categorize_score(score)
        if group:
            counts[group] += 1

    return group_labels, [counts[label] for label in group_labels]


def create_infographic(group_labels, counts, score_list, total_participants, output_file):
    """Create and save the infographic using matplotlib."""
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor("#F8F9FA")

    # Main title
    fig.suptitle(
        "Quiz Score Infographic\nProgramming Fundamentals",
        fontsize=20,
        fontweight="bold",
        color="#2C3E50",
        y=0.98,
    )

    # Left subplot: bar chart
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_facecolor("#FFFFFF")
    bars = ax1.bar(
        group_labels,
        counts,
        color=COLORS,
        edgecolor="white",
        linewidth=1.5,
        width=0.65,
    )

    for bar, count in zip(bars, counts):
        if count > 0:
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.15,
                str(count),
                ha="center",
                va="bottom",
                fontsize=13,
                fontweight="bold",
                color="#2C3E50",
            )

    ax1.set_title("Number of Participants per Score Group", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Score Group", fontsize=11)
    ax1.set_ylabel("Number of Participants", fontsize=11)
    ax1.set_ylim(0, max(counts) + 2 if counts else 1)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Right subplot: pie chart
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_facecolor("#FFFFFF")

    pie_data = [(label, count) for label, count in zip(group_labels, counts) if count > 0]
    if pie_data:
        pie_labels, pie_sizes = zip(*pie_data)
        pie_colors = [COLORS[group_labels.index(label)] for label in pie_labels]
        wedges, texts, autotexts = ax2.pie(
            pie_sizes,
            labels=pie_labels,
            autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
            startangle=90,
            colors=pie_colors,
            explode=[0.03] * len(pie_sizes),
            textprops={"fontsize": 10},
            wedgeprops={"edgecolor": "white", "linewidth": 2},
        )
        for autotext in autotexts:
            autotext.set_fontweight("bold")
            autotext.set_color("white")

    ax2.set_title("Percentage by Score Group", fontsize=14, fontweight="bold", pad=12)

    # Summary statistics at the bottom
    average_score = sum(score_list) / len(score_list) if score_list else 0
    highest_score = max(score_list) if score_list else 0
    lowest_score = min(score_list) if score_list else 0

    info_text = (
        f"Total Participants: {total_participants}  |  "
        f"Average: {average_score:.1f}  |  "
        f"Highest: {highest_score:.1f}  |  "
        f"Lowest: {lowest_score:.1f}"
    )
    fig.text(0.5, 0.02, info_text, ha="center", fontsize=11, color="#555555")

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    plt.savefig(output_file, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Infographic saved to: {output_file}")
    plt.close(fig)


if __name__ == "__main__":
    folder = Path(__file__).parent
    excel_file = folder / "score-quiz.xlsx"
    output_file = folder / "quiz_infographic.png"

    df = pd.read_excel(excel_file)
    score_column = get_score_column(df)
    score_data = df[score_column].apply(parse_score).dropna().tolist()

    group_labels, counts = count_per_group(score_data)

    print("\n=== Quiz Score Distribution ===")
    for label, count in zip(group_labels, counts):
        percentage = (count / len(score_data) * 100) if score_data else 0
        print(f"  {label:>10}: {count:>2} participants ({percentage:.1f}%)")
    print(f"\nTotal: {len(score_data)} participants")

    create_infographic(group_labels, counts, score_data, len(score_data), output_file)