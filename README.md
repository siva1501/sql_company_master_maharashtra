# Company Master – Maharashtra (SQL Analytics)

A pure SQL project analyzing the Maharashtra Company Master open dataset. Corporate records across Maharashtra are analyzed using SQLite to tell a comprehensive story about authorized capital distribution, annual registration trends, district-level registrations in 2015, and the top industrial business activities over time.

---

## Directory Structure

```text
SQL-Company Master - Maharashtra/
│
├── Db_set/                               # Database setup & storage
│   ├── schema.sql                        # DDL table schema and database indexes
│   ├── load_data.sql                     # SQLite data loading script
│   └── company_master.db                 # Pre-populated SQLite database (indexed)
│
├── data/                                 # Raw and reference CSV files
│   ├── company_master_data_2026-09-12.csv # Raw Maharashtra company master dataset
│   └── zip_code_MH.csv                   # Zip code vs district reference mapping
│
├── src/                                  # Main SQL programs
│   ├── 1_authorized_capital.sql          # Problem 1: Histogram of Authorized Capital
│   ├── 2_registration_by_year.sql        # Problem 2: Company registrations by year
│   ├── 3_registration_by_district.sql    # Problem 3: 2015 registrations by district
│   ├── 4_grouped_bar_plot.sql            # Problem 4: Top 5 activities over 2015-2025
│   └── all_queries.sql                   # All 4 analytical queries in a single file
│
├── output/                               # Formatted query execution results (.txt)
│   ├── 1_authorized_capital.txt          # Formatted table: Authorized capital intervals
│   ├── 2_registration_by_year.txt        # Formatted table: Registrations per year (1863-2025)
│   ├── 3_registration_by_district.txt    # Formatted table: 2015 registrations by district
│   └── 4_grouped_bar_plot.txt            # Formatted table: Grouped activities by year
│
├── .gitignore                            # Git ignore rules
└── README.md                             # Project documentation
```

---

## Analytical Problems & Queries

### 1. Histogram of Authorized Capital
- **Query File**: [`src/1_authorized_capital.sql`](src/1_authorized_capital.sql)
- **Output File**: [`output/1_authorized_capital.txt`](output/1_authorized_capital.txt)
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

---

### 2. Company Registrations by Year
- **Query File**: [`src/2_registration_by_year.sql`](src/2_registration_by_year.sql)
- **Output File**: [`output/2_registration_by_year.txt`](output/2_registration_by_year.txt)
- **Columns**: `registration_year | company_count`
- **Description**: Extracts the 4-digit registration year from `registration_date` and counts company registrations chronologically from 1863 to 2025 (144 rows).
- **Sample Output**:
```text
 registration_year | company_count 
-------------------+---------------
              1863 |             1
              1871 |             2
              1872 |             1
              1873 |             3
              1874 |             1
              ...  |           ...
              2021 |         31232
              2022 |         32085
              2023 |         28388
              2024 |         29338
              2025 |         14177
(144 rows)
```

---

### 3. Company Registrations in 2015 by District
- **Query File**: [`src/3_registration_by_district.sql`](src/3_registration_by_district.sql)
- **Output File**: [`output/3_registration_by_district.txt`](output/3_registration_by_district.txt)
- **Columns**: `district | registration_count`
- **Description**: Joins `company_master` with `zip_code_district` on postal code for the year 2015, aggregated and sorted descending by registration count.
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

---

### 4. Grouped Analysis: Top 5 Business Activities (2015 - 2025)
- **Query File**: [`src/4_grouped_bar_plot.sql`](src/4_grouped_bar_plot.sql)
- **Output File**: [`output/4_grouped_bar_plot.txt`](output/4_grouped_bar_plot.txt)
- **Columns**: `reg_year | companyindustrialclassification | registrations_count`
- **Description**: Aggregates registration counts across 2015 to 2025 for the top 5 activities (*Business Services*, *Community, personal and Social Services*, *Trading*, *Agriculture and Allied Activities*, *Manufacturing (Metals and Chemicals, and products thereof)*) resulting in 55 rows.
- **Sample Output**:
```text
 reg_year | companyindustrialclassification                            | registrations_count 
----------+------------------------------------------------------------+---------------------
     2015 | Business Services                                          |                8161
     2015 | Agriculture and Allied Activities                          |                 948
     2015 | Trading                                                    |                 943
     2015 | Community, personal and Social Services                    |                 775
     2015 | Manufacturing (Metals and Chemicals, and products thereof) |                 474
     ...  | ...                                                        |                 ...
     2025 | Community, personal and Social Services                    |                3815
     2025 | Trading                                                    |                2016
     2025 | Business Services                                          |                1785
     2025 | Agriculture and Allied Activities                          |                1343
     2025 | Manufacturing (Metals and Chemicals, and products thereof) |                 729
(55 rows)
```

---

## How to Run the SQL Queries

### Option 1: SQLite Command Line Interface (CLI)

Run individual queries:
```bash
sqlite3 Db_set/company_master.db < src/1_authorized_capital.sql
sqlite3 Db_set/company_master.db < src/2_registration_by_year.sql
sqlite3 Db_set/company_master.db < src/3_registration_by_district.sql
sqlite3 Db_set/company_master.db < src/4_grouped_bar_plot.sql
```

Run all queries together:
```bash
sqlite3 Db_set/company_master.db < src/all_queries.sql
```

---

### Option 2: In VS Code (SQLite Extension)

1. Open the **Extensions** view (`Ctrl + Shift + X`) in VS Code and install **SQLite** (`alexcvzz.vscode-sqlite`) or **SQLTools**.
2. Open any query file in [`src/`](src/) (such as [`src/1_authorized_capital.sql`](src/1_authorized_capital.sql) or [`src/all_queries.sql`](src/all_queries.sql)).
3. Right-click anywhere in the editor and click **"Run Query"** (or press `Ctrl + Shift + Q`).
4. Select `Db_set/company_master.db` when prompted to view live tabular results.

---

### Option 3: GUI Database Tools (DB Browser for SQLite / DBeaver)

1. Open **DB Browser for SQLite** or **DBeaver**.
2. Choose **Open Database** and select [`Db_set/company_master.db`](Db_set/company_master.db).
3. Switch to the **Execute SQL** tab, open or paste any query from [`src/`](src/), and run.
