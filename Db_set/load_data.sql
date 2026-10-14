-- SQL Script to Load Data into Maharashtra Company Master Database
-- Location: Db_set/load_data.sql
-- Usage with SQLite CLI:
--   sqlite3 Db_set/company_master.db < Db_set/load_data.sql

.mode csv

-- Load Postal Code / District mapping
.import --skip 1 data/zip_code_MH.csv zip_code_district

-- Note: company_master table is populated from data/company_master_data_2026-09-12.csv
-- with parsed fields (pin_code, registration_year, authorized_capital) via:
--   python src/run_queries.py
