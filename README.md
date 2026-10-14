# Company Master – Maharashtra (SQL Analytics)

This project provides pure SQL analytics and visualization for the Maharashtra Company Master open dataset. It analyzes corporate records across Maharashtra to tell a comprehensive story about authorized capital distribution, annual registration trends, district-level registrations in 2015, and industrial activity evolution over time.

---

## Directory Structure

```text
SQL-Company Master - Maharashtra/
│
├── Db_set/                               # Database setup & storage
│   ├── schema.sql                        # DDL table schema and database indexes
│   ├── load_data.sql                     # SQLite CLI data import script
│   └── company_master.db                 # Pre-populated SQLite database (indexed)
│
├── data/                                 # Raw and reference CSV files
│   ├── company_master_data_2026-09-12.csv # Raw Maharashtra company master dataset
│   └── zip_code_MH.csv                   # Zip code vs district reference mapping
│
├── src/                                  # Main SQL programs and runners
│   ├── 1_authorized_capital.sql          # Problem 1: Histogram of Authorized Capital
│   ├── 2_registration_by_year.sql        # Problem 2: Company registrations by year
│   ├── 3_registration_by_district.sql    # Problem 3: 2015 registrations by district
│   ├── 4_grouped_bar_plot.sql            # Problem 4: Top 5 activities over 2015-2025
│   ├── all_queries.sql                   # All 4 analytical queries in a single file
│   ├── setup_database.py                 # Database population and verification script
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
- **Columns**: `capital_range | company_count`
- **Output**:
```text
 capital_range | company_count
---------------+---------------
 <= 1L         |        242735
 1L to 10L     |        188239
 10L to 1Cr    |         79901
 1Cr to 10Cr   |         31527
 > 10Cr        |         11668
(5 rows)
```

### 2. Company Registrations by Year
- **File**: [`src/2_registration_by_year.sql`](src/2_registration_by_year.sql)
- **Output Table**: [`output/2_registration_by_year.txt`](output/2_registration_by_year.txt)
- **Chart**: [`output/2_registration_by_year.png`](output/2_registration_by_year.png)
- **Columns**: `registration_year | company_count`
- **Description**: Extracts the 4-digit registration year from `registration_date` and counts company registrations chronologically from 1863 to 2025 (144 rows).

### 3. Company Registrations in 2015 by District
- **File**: [`src/3_registration_by_district.sql`](src/3_registration_by_district.sql)
- **Output Table**: [`output/3_registration_by_district.txt`](output/3_registration_by_district.txt)
- **Chart**: [`output/3_registration_by_district.png`](output/3_registration_by_district.png)
- **Columns**: `district | registration_count`
- **Output**:
```text
  district   | registration_count
-------------+--------------------
  Thane      |                441
  Aurangabad |                193
  Mumbai     |                132
  Pune       |                124
  Palghar    |                 72
  Latur      |                 68
  Sangli     |                 51
  Jalgaon    |                 51
  Ahmednagar |                 48
  Nashik     |                 45
  Kolhapur   |                 33
  Nagpur     |                 27
  Akola      |                 19
  Chandrapur |                 18
  Dhule      |                 17
  Amravati   |                 16
  Parbhani   |                 11
  Solapur    |                  8
  Nanded     |                  4
(19 rows)
```

### 4. Grouped Analysis: Top 5 Business Activities (2015 - 2025)
- **File**: [`src/4_grouped_bar_plot.sql`](src/4_grouped_bar_plot.sql)
- **Output Table**: [`output/4_grouped_bar_plot.txt`](output/4_grouped_bar_plot.txt)
- **Chart**: [`output/4_grouped_bar_plot.png`](output/4_grouped_bar_plot.png)
- **Columns**: `reg_year | companyindustrialclassification | registrations_count`
- **Description**: Aggregates registration counts across 2015 to 2025 for the top 5 activities (*Business Services*, *Community, personal and Social Services*, *Trading*, *Agriculture and Allied Activities*, *Manufacturing (Metals and Chemicals, and products thereof)*) resulting in 55 rows.

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
   - Automatically initializes and indexes `Db_set/company_master.db`.
   - Executes all 4 SQL query files.
   - Formats query results into PostgreSQL / psql-style ASCII tables and writes them to `output/*.txt`.

2. **Generate Matplotlib Charts**:
   ```powershell
   python src/plots.py
   ```
   - Reads query results from `Db_set/company_master.db`.
   - Saves high-resolution visualization charts to `output/*.png`.

### Method 2: SQLite Command Line

```powershell
# Run individual queries
sqlite3 Db_set/company_master.db < src/1_authorized_capital.sql
sqlite3 Db_set/company_master.db < src/2_registration_by_year.sql
sqlite3 Db_set/company_master.db < src/3_registration_by_district.sql
sqlite3 Db_set/company_master.db < src/4_grouped_bar_plot.sql

# Run all queries
sqlite3 Db_set/company_master.db < src/all_queries.sql
```

### Method 3: In VS Code (SQLite Extension)

1. Install the **`SQLite`** extension (`alexcvzz.vscode-sqlite`) from VS Code Extensions (`Ctrl + Shift + X`).
2. Open any query file in `src/` (e.g. [`src/1_authorized_capital.sql`](src/1_authorized_capital.sql) or [`src/all_queries.sql`](src/all_queries.sql)).
3. **Right-click** anywhere in the query editor and choose **"Run Query"** (or press `Ctrl + Shift + Q`).
4. Select `Db_set/company_master.db` as the database to view live interactive results.
