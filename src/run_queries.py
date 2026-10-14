"""
Runner script to execute SQL analytical queries for Company Master.

Loads data from CSV files into a local SQLite database if not already
present, executes each SQL query file, and generates psql-styled
tabular reports into the output directory.
"""

import csv
from pathlib import Path
import re
import sqlite3
import time

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = BASE_DIR / "company_master.db"
SCHEMA_SQL = SRC_DIR / "schema.sql"
ZIP_CSV = DATA_DIR / "zip_code_MH.csv"
COMPANY_CSV = DATA_DIR / "company_master_data_2026-09-12.csv"


def extract_pin_code(address: str) -> str:
    """Extract the last 6-digit PIN code found in the address."""
    if not address:
        return ""
    pins = re.findall(r"\b\d{6}\b", address)
    return pins[-1] if pins else ""


def parse_year(date_str: str) -> int | None:
    """Extract 4-digit registration year from date string."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    if len(cleaned) >= 4 and cleaned[:4].isdigit():
        year = int(cleaned[:4])
        if 1800 <= year <= 2100:
            return year
    return None


def init_database(conn: sqlite3.Connection) -> None:
    """Ensure database schema and data are fully loaded and indexed."""
    cursor = conn.cursor()

    cursor.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table' "
        "AND name='company_master'"
    )
    has_table = cursor.fetchone()[0] > 0
    row_count = 0
    if has_table:
        cursor.execute("SELECT count(*) FROM company_master")
        row_count = cursor.fetchone()[0]

    if has_table and row_count > 0:
        return

    print("Initializing database from schema...")
    with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # Load zip_code_district
    if ZIP_CSV.exists():
        print(f"Loading {ZIP_CSV.name}...")
        zip_records = []
        with open(ZIP_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                pin = r.get("Pin Code", "").strip()
                city = r.get("City/Town", "").strip()
                district = r.get("District", "").strip()
                state = r.get("State", "").strip()
                country = r.get("Country", "").strip()
                if pin and district:
                    zip_records.append((pin, city, district, state, country))

        cursor.executemany(
            "INSERT OR REPLACE INTO zip_code_district "
            "(pin_code, city_town, district, state, country) "
            "VALUES (?, ?, ?, ?, ?)",
            zip_records,
        )
        conn.commit()
        print(f"Loaded {len(zip_records)} postal codes.")

    # Load company_master
    if COMPANY_CSV.exists():
        print(f"Loading {COMPANY_CSV.name} (this may take a few seconds)...")
        t0 = time.time()
        batch = []
        batch_size = 25000
        total = 0

        with open(COMPANY_CSV, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cin = r.get("CIN", "").strip()
                if not cin:
                    continue
                name = r.get("Company Name", "").strip()
                reg_date = r.get("Company Registration Date", "").strip()
                reg_year = parse_year(reg_date)
                cat = r.get("Company Category", "").strip()
                c_class = r.get("Company Class", "").strip()
                list_stat = r.get("Listing Status", "").strip()
                try:
                    auth_cap = float(r.get("Authorized Capital", 0) or 0)
                except ValueError:
                    auth_cap = 0.0
                try:
                    paid_cap = float(r.get("Paidup Capital", 0) or 0)
                except ValueError:
                    paid_cap = 0.0
                roc = r.get("Company ROC", "").strip()
                addr = r.get("Company Address", "").strip()
                pin = extract_pin_code(addr)
                c_state = r.get("Company State", "").strip()
                c_stat = r.get("Company Status", "").strip()
                sub_cat = r.get("Company Sub Category", "").strip()
                ind_class = r.get(
                    "Company Industrial Classification", ""
                ).strip()

                batch.append((
                    cin,
                    name,
                    reg_date,
                    reg_year,
                    cat,
                    c_class,
                    list_stat,
                    auth_cap,
                    paid_cap,
                    roc,
                    addr,
                    pin,
                    c_state,
                    c_stat,
                    sub_cat,
                    ind_class,
                ))

                if len(batch) >= batch_size:
                    cursor.executemany(
                        "INSERT OR IGNORE INTO company_master ("
                        "cin, company_name, registration_date, "
                        "registration_year, company_category, company_class, "
                        "listing_status, authorized_capital, paidup_capital, "
                        "company_roc, company_address, pin_code, "
                        "company_state, company_status, company_sub_category, "
                        "industrial_classification) VALUES ("
                        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        batch,
                    )
                    conn.commit()
                    total += len(batch)
                    batch = []

            if batch:
                cursor.executemany(
                    "INSERT OR IGNORE INTO company_master ("
                    "cin, company_name, registration_date, "
                    "registration_year, company_category, company_class, "
                    "listing_status, authorized_capital, paidup_capital, "
                    "company_roc, company_address, pin_code, "
                    "company_state, company_status, company_sub_category, "
                    "industrial_classification) VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    batch,
                )
                conn.commit()
                total += len(batch)

        elapsed = time.time() - t0
        print(f"Loaded {total:,} companies into database in {elapsed:.2f}s.")


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
    lines.append("|".join(header_parts))

    sep_parts = ["-" * (w + 2) for w in col_widths]
    lines.append("+".join(sep_parts))

    for r in str_rows:
        row_parts = []
        for col_idx, val in enumerate(r):
            w = col_widths[col_idx]
            is_num = numeric_cols[col_idx]
            formatted = val.rjust(w) if is_num else val.ljust(w)
            row_parts.append(f" {formatted} ")
        lines.append("|".join(row_parts))

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
    conn = sqlite3.connect(str(DB_PATH))
    try:
        init_database(conn)

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
