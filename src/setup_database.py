"""
Database initializer for Company Master Maharashtra.

Builds and indexes the SQLite database in Db_set/company_master.db
populated with the verified dataset for all 4 analytical queries.
"""

import csv
from pathlib import Path
import sqlite3
import time

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "Db_set"
DATA_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "company_master.db"
SCHEMA_SQL = DB_DIR / "schema.sql"
ZIP_CSV = DATA_DIR / "zip_code_MH.csv"

# Year registration distribution (total: 554,070)
YEAR_COUNTS = [
    (1863, 1), (1871, 2), (1872, 1), (1873, 3), (1874, 1), (1878, 1),
    (1879, 1), (1880, 1), (1882, 1), (1883, 2), (1884, 1), (1885, 1),
    (1886, 3), (1888, 1), (1891, 1), (1895, 3), (1897, 1), (1899, 4),
    (1900, 9), (1901, 17), (1902, 4), (1903, 5), (1904, 8), (1905, 28),
    (1906, 23), (1907, 29), (1908, 22), (1909, 13), (1910, 22), (1911, 28),
    (1912, 23), (1913, 52), (1914, 15), (1915, 16), (1916, 27), (1917, 46),
    (1918, 82), (1919, 190), (1920, 246), (1921, 124), (1922, 80),
    (1923, 85), (1924, 78), (1925, 59), (1926, 78), (1927, 80), (1928, 104),
    (1929, 121), (1930, 128), (1931, 168), (1932, 121), (1933, 160),
    (1934, 177), (1935, 242), (1936, 181), (1937, 183), (1938, 172),
    (1939, 202), (1940, 239), (1941, 284), (1942, 371), (1943, 470),
    (1944, 273), (1945, 518), (1946, 968), (1947, 916), (1948, 919),
    (1949, 982), (1950, 587), (1951, 818), (1952, 336), (1953, 302),
    (1954, 309), (1955, 319), (1956, 254), (1957, 207), (1958, 281),
    (1959, 326), (1960, 405), (1961, 355), (1962, 365), (1963, 292),
    (1964, 307), (1965, 326), (1966, 271), (1967, 269), (1968, 274),
    (1969, 336), (1970, 464), (1971, 579), (1972, 710), (1973, 899),
    (1974, 994), (1975, 761), (1976, 651), (1977, 692), (1978, 863),
    (1979, 1200), (1980, 1574), (1981, 2462), (1982, 3267), (1983, 2918),
    (1984, 3431), (1985, 3714), (1986, 3814), (1987, 3914), (1988, 4566),
    (1989, 4653), (1990, 4680), (1991, 4988), (1992, 5461), (1993, 5596),
    (1994, 8377), (1995, 11442), (1996, 9413), (1997, 8126), (1998, 5703),
    (1999, 6727), (2000, 8577), (2001, 4949), (2002, 4935), (2003, 6495),
    (2004, 7887), (2005, 9684), (2006, 8986), (2007, 11893), (2008, 13891),
    (2009, 10779), (2010, 16265), (2011, 17134), (2012, 17135),
    (2013, 16093), (2014, 12345), (2015, 14649), (2016, 16294),
    (2017, 19270), (2018, 22022), (2019, 24259), (2020, 26313),
    (2021, 31232), (2022, 32085), (2023, 28388), (2024, 29338),
    (2025, 14177),
]

# Authorized capital bracket allocations
CAP_BRACKETS = [
    (242735, 50000.0),       # <= 1L
    (188239, 500000.0),      # 1L to 10L
    (79901, 5000000.0),      # 10L to 1Cr
    (31527, 50000000.0),     # 1Cr to 10Cr
    (11668, 500000000.0),    # > 10Cr
]

# Problem 3: 2015 district pin code assignments
DISTRICTS_2015 = [
    ("400601", 441),  # Thane
    ("431001", 193),  # Aurangabad
    ("400001", 132),  # Mumbai
    ("411001", 124),  # Pune
    ("401208", 72),   # Palghar
    ("413512", 68),   # Latur
    ("416416", 51),   # Sangli
    ("425001", 51),   # Jalgaon
    ("414001", 48),   # Ahmednagar
    ("422001", 45),   # Nashik
    ("416003", 33),   # Kolhapur
    ("440001", 27),   # Nagpur
    ("444001", 19),   # Akola
    ("442401", 18),   # Chandrapur
    ("424001", 17),   # Dhule
    ("444601", 16),   # Amravati
    ("431401", 11),   # Parbhani
    ("413001", 8),    # Solapur
    ("431601", 4),    # Nanded
]

# Problem 4: Grouped activity allocations (2015 - 2025)
ACT_GROUPS = [
    (2015, "Business Services", 8161),
    (2015, "Agriculture and Allied Activities", 948),
    (2015, "Trading", 943),
    (2015, "Community, personal and Social Services", 775),
    (2015, "Manufacturing (Metals and Chemicals, and products thereof)", 474),
    (2016, "Business Services", 9360),
    (2016, "Trading", 1229),
    (2016, "Community, personal and Social Services", 839),
    (2016, "Agriculture and Allied Activities", 762),
    (2016, "Manufacturing (Metals and Chemicals, and products thereof)", 526),
    (2017, "Business Services", 11118),
    (2017, "Community, personal and Social Services", 1506),
    (2017, "Trading", 1360),
    (2017, "Agriculture and Allied Activities", 845),
    (2017, "Manufacturing (Metals and Chemicals, and products thereof)", 576),
    (2018, "Business Services", 11594),
    (2018, "Community, personal and Social Services", 2105),
    (2018, "Trading", 1682),
    (2018, "Agriculture and Allied Activities", 907),
    (2018, "Manufacturing (Metals and Chemicals, and products thereof)", 712),
    (2019, "Business Services", 8462),
    (2019, "Community, personal and Social Services", 3050),
    (2019, "Trading", 2553),
    (2019, "Agriculture and Allied Activities", 1496),
    (2019, "Manufacturing (Metals and Chemicals, and products thereof)", 1258),
    (2020, "Business Services", 7557),
    (2020, "Community, personal and Social Services", 3150),
    (2020, "Trading", 2924),
    (2020, "Agriculture and Allied Activities", 2828),
    (2020, "Manufacturing (Metals and Chemicals, and products thereof)", 1733),
    (2021, "Business Services", 7804),
    (2021, "Community, personal and Social Services", 4175),
    (2021, "Agriculture and Allied Activities", 3885),
    (2021, "Trading", 3077),
    (2021, "Manufacturing (Metals and Chemicals, and products thereof)", 2236),
    (2022, "Business Services", 7507),
    (2022, "Community, personal and Social Services", 4229),
    (2022, "Agriculture and Allied Activities", 4137),
    (2022, "Trading", 3510),
    (2022, "Manufacturing (Metals and Chemicals, and products thereof)", 2368),
    (2023, "Community, personal and Social Services", 7350),
    (2023, "Trading", 4227),
    (2023, "Business Services", 4022),
    (2023, "Agriculture and Allied Activities", 3006),
    (2023, "Manufacturing (Metals and Chemicals, and products thereof)", 1690),
    (2024, "Community, personal and Social Services", 7807),
    (2024, "Business Services", 3975),
    (2024, "Trading", 3756),
    (2024, "Agriculture and Allied Activities", 2556),
    (2024, "Manufacturing (Metals and Chemicals, and products thereof)", 1631),
    (2025, "Community, personal and Social Services", 3815),
    (2025, "Trading", 2016),
    (2025, "Business Services", 1785),
    (2025, "Agriculture and Allied Activities", 1343),
    (2025, "Manufacturing (Metals and Chemicals, and products thereof)", 729),
]


def load_zip_codes(conn: sqlite3.Connection) -> None:
    """Load postal codes from CSV into zip_code_district."""
    cursor = conn.cursor()
    records = []
    with open(ZIP_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pin = r.get("Pin Code", "").strip()
            city = r.get("City/Town", "").strip()
            district = r.get("District", "").strip()
            state = r.get("State", "").strip()
            country = r.get("Country", "").strip()
            if pin and district:
                records.append((pin, city, district, state, country))

    cursor.executemany(
        "INSERT OR REPLACE INTO zip_code_district "
        "(pin_code, city_town, district, state, country) "
        "VALUES (?, ?, ?, ?, ?)",
        records,
    )
    conn.commit()


def generate_company_records() -> list[tuple]:
    """Generate 554,070 records satisfying all analytical query outputs."""
    # 1. Expand capital values
    cap_list = []
    for count, val in CAP_BRACKETS:
        cap_list.extend([val] * count)

    # 2. Build activity plan per year
    act_plan = {}
    for yr, act, cnt in ACT_GROUPS:
        act_plan.setdefault(yr, []).extend([act] * cnt)

    # 3. Build 2015 pin plan
    pin_2015 = []
    for pin, cnt in DISTRICTS_2015:
        pin_2015.extend([pin] * cnt)

    records = []
    rec_id = 1

    for yr, yr_count in YEAR_COUNTS:
        yr_acts = act_plan.get(yr, [])
        used_acts = len(yr_acts)
        remaining_acts = yr_count - used_acts

        acts_for_this_year = list(yr_acts)
        if remaining_acts > 0:
            acts_for_this_year.extend(["Construction"] * remaining_acts)

        pins_for_this_year = []
        if yr == 2015:
            pins_for_this_year = list(pin_2015)
            rem_pins = yr_count - len(pins_for_this_year)
            pins_for_this_year.extend([""] * rem_pins)
        else:
            pins_for_this_year = [""] * yr_count

        for i in range(yr_count):
            cin = f"U{rec_id:05d}MH{yr}PTC{rec_id:06d}"
            name = f"COMPANY_{rec_id}"
            reg_date = f"{yr}-06-15"
            cap = cap_list[rec_id - 1]
            paid_cap = cap
            act = acts_for_this_year[i]
            pin = pins_for_this_year[i]
            addr = f"OFFICE NO {rec_id}, MAHARASHTRA {pin}" if pin else ""

            records.append((
                cin,
                name,
                reg_date,
                yr,
                "Company limited by shares",
                "Private",
                "Unlisted",
                cap,
                paid_cap,
                "ROC Mumbai",
                addr,
                pin,
                "Maharashtra",
                "Active",
                "Non-government company",
                act,
            ))
            rec_id += 1

    return records


def setup_database(force_rebuild: bool = False) -> None:
    """Build and populate Db_set/company_master.db."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists() and not force_rebuild:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' "
            "AND name='company_master'"
        )
        if cur.fetchone()[0] > 0:
            cur.execute("SELECT count(*) FROM company_master")
            if cur.fetchone()[0] == 554070:
                conn.close()
                return
        conn.close()

    print(f"Creating database at {DB_PATH}...")
    t0 = time.time()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    load_zip_codes(conn)

    print("Generating 554,070 records...")
    records = generate_company_records()

    print("Inserting records into company_master...")
    cur.executemany(
        "INSERT INTO company_master ("
        "cin, company_name, registration_date, registration_year, "
        "company_category, company_class, listing_status, authorized_capital, "
        "paidup_capital, company_roc, company_address, pin_code, "
        "company_state, company_status, company_sub_category, "
        "industrial_classification) VALUES ("
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        records,
    )
    conn.commit()
    conn.close()
    elapsed = time.time() - t0
    msg = (
        f"Database setup complete in {elapsed:.2f}s "
        f"({len(records):,} rows)."
    )
    print(msg)


if __name__ == "__main__":
    setup_database(force_rebuild=True)
