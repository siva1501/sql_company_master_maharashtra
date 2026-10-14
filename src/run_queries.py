"""
Runner script to execute SQL analytical queries for Company Master.

Connects to the database in Db_set/company_master.db, executes all
SQL analytical query files, and formats the output into PostgreSQL /
psql-style tabular reports in the output directory.
"""

from pathlib import Path
import sqlite3

from setup_database import setup_database

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "Db_set"
SRC_DIR = BASE_DIR / "src"
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = DB_DIR / "company_master.db"


def format_psql_table(
    headers: list[str],
    rows: list[tuple],
    numeric_cols: list[bool],
) -> str:
    """Format query rows into exact PostgreSQL / psql table format."""
    str_rows = []
    for row in rows:
        row_strs = []
        for val in row:
            if isinstance(val, float) and val.is_integer():
                row_strs.append(str(int(val)))
            elif val is None:
                row_strs.append("")
            else:
                row_strs.append(str(val))
        str_rows.append(row_strs)

    col_widths = []
    for col_idx, h in enumerate(headers):
        max_w = len(h)
        for r in str_rows:
            if col_idx < len(r):
                max_w = max(max_w, len(r[col_idx]))
        col_widths.append(max_w)

    lines = []
    header_parts = []
    for col_idx, h in enumerate(headers):
        w = col_widths[col_idx]
        is_num = numeric_cols[col_idx]
        formatted = h.rjust(w) if is_num else h.ljust(w)
        header_parts.append(f" {formatted} ")
    lines.append("|".join(header_parts).rstrip())

    sep_parts = ["-" * (w + 2) for w in col_widths]
    lines.append("+".join(sep_parts))

    for r in str_rows:
        row_parts = []
        for col_idx, val in enumerate(r):
            w = col_widths[col_idx]
            is_num = numeric_cols[col_idx]
            formatted = val.rjust(w) if is_num else val.ljust(w)
            row_parts.append(f" {formatted} ")
        lines.append("|".join(row_parts).rstrip())

    count_str = f"({len(rows)} row{'s' if len(rows) != 1 else ''})"
    lines.append(count_str)
    return "\n".join(lines) + "\n"


def execute_query_file(
    conn: sqlite3.Connection,
    sql_file: Path,
    output_file: Path,
) -> None:
    """Execute SQL query from file and write formatted output."""
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    numeric_cols = []
    for col_idx in range(len(headers)):
        is_num = True
        for row in rows:
            val = row[col_idx]
            if val is not None and not isinstance(val, (int, float)):
                is_num = False
                break
        numeric_cols.append(is_num)

    table_txt = format_psql_table(headers, rows, numeric_cols)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(table_txt)

    print(f"[OK] {sql_file.name} -> {output_file.name} ({len(rows)} rows)")


def main() -> None:
    """Run all analytical SQL queries."""
    if not DB_PATH.exists():
        setup_database()

    conn = sqlite3.connect(str(DB_PATH))
    try:
        queries = [
            ("1_authorized_capital.sql", "1_authorized_capital.txt"),
            ("2_registration_by_year.sql", "2_registration_by_year.txt"),
            (
                "3_registration_by_district.sql",
                "3_registration_by_district.txt",
            ),
            ("4_grouped_bar_plot.sql", "4_grouped_bar_plot.txt"),
        ]

        print("\nExecuting analytical SQL queries...")
        for sql_name, out_name in queries:
            sql_path = SRC_DIR / sql_name
            out_path = OUTPUT_DIR / out_name
            execute_query_file(conn, sql_path, out_path)

        print("\nAll SQL queries executed successfully!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
