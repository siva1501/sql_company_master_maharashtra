"""
Plotting module to visualize Company Master Maharashtra analytics.

Reads data from the local SQLite database and generates 4 publication-quality
matplotlib charts saved into the output directory.
"""

from collections import defaultdict
from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = BASE_DIR / "company_master.db"


def plot_authorized_capital(conn: sqlite3.Connection) -> None:
    """Generate histogram bar chart of company authorized capital."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            CASE
                WHEN authorized_capital <= 100000 THEN '<= 1L'
                WHEN authorized_capital <= 1000000 THEN '1L to 10L'
                WHEN authorized_capital <= 10000000 THEN '10L to 1Cr'
                WHEN authorized_capital <= 100000000 THEN '1Cr to 10Cr'
                ELSE '> 10Cr'
            END AS capital_range,
            COUNT(*) AS count
        FROM company_master
        WHERE authorized_capital IS NOT NULL
        GROUP BY capital_range
        ORDER BY
            CASE capital_range
                WHEN '<= 1L' THEN 1
                WHEN '1L to 10L' THEN 2
                WHEN '10L to 1Cr' THEN 3
                WHEN '1Cr to 10Cr' THEN 4
                WHEN '> 10Cr' THEN 5
            END;
    """)
    rows = cursor.fetchall()
    categories = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(10, 6))
    colors = ["#2b5c8f", "#3c7ebf", "#5b9bd5", "#8bbbe8", "#b8d5f2"]
    bars = plt.bar(
        categories,
        counts,
        color=colors,
        edgecolor="#1b3c5f",
        width=0.6,
    )

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 3000,
            f"{int(height):,}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    plt.title(
        "Histogram of Authorized Capital (Maharashtra)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Authorized Capital Interval", fontsize=11, labelpad=10)
    plt.ylabel("Number of Companies", fontsize=11, labelpad=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_file = OUTPUT_DIR / "1_authorized_capital.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generated plot: {out_file.name}")


def plot_registration_by_year(conn: sqlite3.Connection) -> None:
    """Generate bar chart of registrations by year."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            registration_year AS year,
            COUNT(*) AS count
        FROM company_master
        WHERE registration_year IS NOT NULL
          AND registration_year >= 1950
          AND registration_year <= 2026
        GROUP BY registration_year
        ORDER BY registration_year ASC;
    """)
    rows = cursor.fetchall()
    years = [str(r[0]) for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(14, 6))
    plt.bar(
        years,
        counts,
        color="#1f77b4",
        edgecolor="#0f4471",
        width=0.7,
    )

    plt.title(
        "Company Registrations by Year in Maharashtra (1950 - 2026)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Year of Registration", fontsize=11, labelpad=10)
    plt.ylabel("Number of Registrations", fontsize=11, labelpad=10)
    plt.xticks(rotation=90, fontsize=8)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_file = OUTPUT_DIR / "2_registration_by_year.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generated plot: {out_file.name}")


def plot_registration_by_district(conn: sqlite3.Connection) -> None:
    """Generate bar chart of 2015 registrations by district."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            z.district AS district,
            COUNT(c.cin) AS count
        FROM company_master c
        JOIN zip_code_district z
            ON c.pin_code = z.pin_code
        WHERE c.registration_year = 2015
        GROUP BY z.district
        ORDER BY count DESC;
    """)
    rows = cursor.fetchall()
    districts = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        districts,
        counts,
        color="#2ca02c",
        edgecolor="#145214",
        width=0.6,
    )

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 5,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
        )

    plt.title(
        "Company Registrations in 2015 by District (Maharashtra)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("District", fontsize=11, labelpad=10)
    plt.ylabel("Number of Registrations", fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_file = OUTPUT_DIR / "3_registration_by_district.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generated plot: {out_file.name}")


def plot_grouped_bar_plot(conn: sqlite3.Connection) -> None:
    """Generate grouped bar plot of top 5 activities for last 10 years."""
    cursor = conn.cursor()
    cursor.execute("""
        WITH last_10_years AS (
            SELECT DISTINCT registration_year
            FROM company_master
            WHERE registration_year IS NOT NULL
              AND registration_year BETWEEN 1900 AND 2026
            ORDER BY registration_year DESC
            LIMIT 10
        ),
        top_5_activities AS (
            SELECT
                c.industrial_classification AS activity,
                COUNT(*) AS total_count
            FROM company_master c
            JOIN last_10_years y
                ON c.registration_year = y.registration_year
            WHERE c.industrial_classification IS NOT NULL
              AND c.industrial_classification != ''
            GROUP BY c.industrial_classification
            ORDER BY total_count DESC
            LIMIT 5
        )
        SELECT
            c.registration_year AS year,
            c.industrial_classification AS activity,
            COUNT(*) AS count
        FROM company_master c
        JOIN last_10_years y
            ON c.registration_year = y.registration_year
        JOIN top_5_activities a
            ON c.industrial_classification = a.activity
        GROUP BY c.registration_year, c.industrial_classification
        ORDER BY c.registration_year ASC, a.total_count DESC;
    """)
    rows = cursor.fetchall()

    year_set = sorted(list({r[0] for r in rows}))
    years = [str(y) for y in year_set]

    activity_order = []
    seen = set()
    for _, act, _ in rows:
        if act not in seen:
            seen.add(act)
            activity_order.append(act)

    data = defaultdict(dict)
    for y, act, cnt in rows:
        data[str(y)][act] = cnt

    num_years = len(years)
    num_activities = len(activity_order)
    width = 0.16
    x_indices = list(range(num_years))

    plt.figure(figsize=(15, 7))
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for idx, act in enumerate(activity_order):
        offsets = [x + (idx - num_activities / 2.0 + 0.5) * width
                   for x in x_indices]
        values = [data[y].get(act, 0) for y in years]
        plt.bar(
            offsets,
            values,
            width=width,
            label=act,
            color=palette[idx % len(palette)],
            edgecolor="#333333",
            linewidth=0.5,
        )

    plt.title(
        "Top 5 Principal Business Activities Over Last 10 Years (Maharashtra)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Year of Registration", fontsize=11, labelpad=10)
    plt.ylabel("Number of Registrations", fontsize=11, labelpad=10)
    plt.xticks(x_indices, years, fontsize=10)
    plt.legend(title="Business Activity", fontsize=9, title_fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_file = OUTPUT_DIR / "4_grouped_bar_plot.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generated plot: {out_file.name}")


def main() -> None:
    """Generate all analytical plots."""
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Please run run_queries.py.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        print("Generating analytical plots...")
        plot_authorized_capital(conn)
        plot_registration_by_year(conn)
        plot_registration_by_district(conn)
        plot_grouped_bar_plot(conn)
        print("All analytical plots generated successfully!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
