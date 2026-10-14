-- Schema Definition for Maharashtra Company Master Database (SQLite)
-- Stored in Db_set/

DROP TABLE IF EXISTS company_master;
DROP TABLE IF EXISTS zip_code_district;

-- Table for Maharashtra Postal Code / Zip Code to District Mapping
CREATE TABLE zip_code_district (
    pin_code TEXT PRIMARY KEY,
    city_town TEXT,
    district TEXT NOT NULL,
    state TEXT,
    country TEXT
);

-- Table for Maharashtra Company Master Records
CREATE TABLE company_master (
    cin TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    registration_date TEXT,
    registration_year INTEGER,
    company_category TEXT,
    company_class TEXT,
    listing_status TEXT,
    authorized_capital REAL DEFAULT 0,
    paidup_capital REAL DEFAULT 0,
    company_roc TEXT,
    company_address TEXT,
    pin_code TEXT,
    company_state TEXT,
    company_status TEXT,
    company_sub_category TEXT,
    industrial_classification TEXT
);

-- Performance Indexes
CREATE INDEX idx_company_reg_year ON company_master(registration_year);
CREATE INDEX idx_company_pin_code ON company_master(pin_code);
CREATE INDEX idx_company_auth_cap ON company_master(authorized_capital);
CREATE INDEX idx_company_ind_class ON company_master(industrial_classification);
CREATE INDEX idx_zip_district ON zip_code_district(district);
