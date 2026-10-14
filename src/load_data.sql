-- SQL Script to Load Data into Maharashtra Company Master Database
-- Usage with SQLite CLI:
--   sqlite3 company_master.db < src/load_data.sql

.mode csv

-- Load Postal Code / District mapping
.import --skip 1 data/zip_code_MH.csv zip_code_district

-- Note: company_master data is automatically populated with clean
-- parsed fields (including pin_code and registration_year) via the
-- high-performance automated runner: python src/run_queries.py
