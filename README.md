# Company Master – Maharashtra (SQL Analytics)

This project provides pure SQL analytics and visualization for the Maharashtra Company Master open dataset sourced from [data.gov.in](https://data.gov.in/catalog/company-master-data). It analyzes over 600,000 corporate entities across Maharashtra to tell a comprehensive story about authorized capital distribution, annual registration trends, district-level registrations in 2015, and industrial activity evolution over the last decade.

---

## Directory Structure

```text
SQL-Company Master - Maharashtra/
│
├── data/                                 # Raw and reference CSV files
│   ├── company_master_data_2026-09-12.csv # Raw Maharashtra company master dataset
│   └── zip_code_MH.csv                   # Zip code vs district reference mapping
│
├── src/                                  # Main SQL programs and runners
│   ├── 1_authorized_capital.sql          # Problem 1: Histogram of Authorized Capital
│   ├── 2_registration_by_year.sql        # Problem 2: Company registrations by year
│   ├── 3_registration_by_district.sql    # Problem 3: 2015 registrations by district
│   ├── 4_grouped_bar_plot.sql            # Problem 4: Top 5 activities over last 10 years
│   ├── all_queries.sql                   # All 4 analytical queries in a single file
│   ├── schema.sql                        # DDL table schema and indexing definitions
│   ├── load_data.sql                     # SQLite CLI data import script
│   ├── run_queries.py                    # Python runner to execute SQL queries and export .txt
│   └── plots.py                          # Matplotlib script to generate .png charts
│
├── output/                               # Query execution results and visualization charts
│   ├── 1_authorized_capital.txt          # Formatted table: Authorized capital intervals
│   ├── 1_authorized_capital.png          # Histogram bar chart: Authorized capital
│   ├── 2_registration_by_year.txt        # Formatted table: Registrations per year
│   ├── 2_registration_by_year.png        # Bar chart: Registrations vs. year
│   ├── 3_registration_by_district.txt    # Formatted table: 2015 registrations by district
│   ├── 3_registration_by_district.png    # Bar chart: 2015 registrations vs. district
│   ├── 4_grouped_bar_plot.txt            # Formatted table: Grouped activities by year
│   └── 4_grouped_bar_plot.png            # Grouped bar chart: Top 5 activities
│
├── company_master.db                     # SQLite database (indexed)
├── requirements.txt                      # Dependencies (matplotlib, flake8)
├── .gitignore                            # Git ignore rules
└── README.md                             # Project documentation
```

---

## Analytical Problems & Queries

### 1. Histogram of Authorized Capital
- **File**: [`src/1_authorized_capital.sql`](src/1_authorized_capital.sql)
- **Output Table**: [`output/1_authorized_capital.txt`](output/1_authorized_capital.txt)
- **Chart**: [`output/1_authorized_capital.png`](output/1_authorized_capital.png)
- **Description**: Buckets all companies into five authorized capital intervals (`<= 1L`, `1L to 10L`, `10L to 1Cr`, `1Cr to 10Cr`, `> 10Cr`) and counts companies in each bracket:
  - `<= 1L`: 268,801
  - `1L to 10L`: 205,461
  - `10L to 1Cr`: 85,653
  - `1Cr to 10Cr`: 33,642
  - `> 10Cr`: 12,791

### 2. Company Registrations by Year
- **File**: [`src/2_registration_by_year.sql`](src/2_registration_by_year.sql)
- **Output Table**: [`output/2_registration_by_year.txt`](output/2_registration_by_year.txt)
- **Chart**: [`output/2_registration_by_year.png`](output/2_registration_by_year.png)
- **Description**: Extracts the 4-digit registration year from `registration_date` and counts company registrations chronologically from 1900 to 2026.

### 3. Company Registrations in 2015 by District
- **File**: [`src/3_registration_by_district.sql`](src/3_registration_by_district.sql)
- **Output Table**: [`output/3_registration_by_district.txt`](output/3_registration_by_district.txt)
- **Chart**: [`output/3_registration_by_district.png`](output/3_registration_by_district.png)
- **Description**: Filters registrations for the year 2015, joins with the postal code mapping table (`zip_code_district`), and aggregates registration counts by district in descending order (led by Thane: 448, Aurangabad: 195, Mumbai: 138, Pune: 114).

### 4. Grouped Analysis: Top 5 Business Activities (Last 10 Years)
- **File**: [`src/4_grouped_bar_plot.sql`](src/4_grouped_bar_plot.sql)
- **Output Table**: [`output/4_grouped_bar_plot.txt`](output/4_grouped_bar_plot.txt)
- **Chart**: [`output/4_grouped_bar_plot.png`](output/4_grouped_bar_plot.png)
- **Description**: Uses Common Table Expressions (CTEs) to isolate the last 10 available years (2017–2026) and identify the top 5 principal industrial classifications (*Business Services*, *Community, personal and Social Services*, *Trading*, *Agriculture and Allied Activities*, *Construction*), aggregating counts per year and activity.

---

## Setup Instructions

### 1. Create and Activate Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate on Windows PowerShell
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Linting (Flake8)

All Python scripts are 100% compliant with PEP8 and flake8 standards:

```powershell
flake8 src/
```

---

## How to Run

### Method 1: Automated Python Runners (Recommended)

1. **Execute All SQL Queries & Export Reports**:
   ```powershell
   python src/run_queries.py
   ```
   - Automatically initializes and indexes `company_master.db` from `data/*.csv`.
   - Executes all 4 SQL query files.
   - Formats query results into PostgreSQL / psql-style ASCII tables and writes them to `output/*.txt`.

2. **Generate Matplotlib Charts**:
   ```powershell
   python src/plots.py
   ```
   - Reads query results from `company_master.db`.
   - Saves high-resolution visualization charts to `output/*.png`.

### Method 2: SQLite Command Line

If you have the SQLite CLI installed:

```powershell
# Run individual queries
sqlite3 company_master.db < src/1_authorized_capital.sql
sqlite3 company_master.db < src/2_registration_by_year.sql
sqlite3 company_master.db < src/3_registration_by_district.sql
sqlite3 company_master.db < src/4_grouped_bar_plot.sql

# Run all queries
sqlite3 company_master.db < src/all_queries.sql
```

### Method 3: In VS Code (SQLite Extension)

1. Install the **`SQLite`** extension (`alexcvzz.vscode-sqlite`) from VS Code Extensions (`Ctrl + Shift + X`).
2. Open any query file in `src/` (e.g. [`src/1_authorized_capital.sql`](src/1_authorized_capital.sql) or [`src/all_queries.sql`](src/all_queries.sql)).
3. **Right-click** anywhere in the query editor and choose **"Run Query"** (or press `Ctrl + Shift + Q`).
4. Select `company_master.db` as the database to view live interactive results.
