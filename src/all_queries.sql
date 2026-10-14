-- ============================================================================
-- All Analytical Queries: Company Master - Maharashtra
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Histogram of Authorized Capital
-- ----------------------------------------------------------------------------
SELECT 
    capital_range,
    company_count
FROM (
    SELECT 
        CASE 
            WHEN authorized_capital <= 100000 THEN '<= 1L'
            WHEN authorized_capital <= 1000000 THEN '1L to 10L'
            WHEN authorized_capital <= 10000000 THEN '10L to 1Cr'
            WHEN authorized_capital <= 100000000 THEN '1Cr to 10Cr'
            ELSE '> 10Cr'
        END AS capital_range,
        COUNT(*) AS company_count
    FROM company_master
    WHERE authorized_capital IS NOT NULL
    GROUP BY capital_range
)
ORDER BY 
    CASE capital_range
        WHEN '<= 1L' THEN 1
        WHEN '1L to 10L' THEN 2
        WHEN '10L to 1Cr' THEN 3
        WHEN '1Cr to 10Cr' THEN 4
        WHEN '> 10Cr' THEN 5
    END;

-- ----------------------------------------------------------------------------
-- 2. Bar Plot of Company Registration by Year
-- ----------------------------------------------------------------------------
SELECT 
    registration_year,
    COUNT(*) AS company_count
FROM company_master
WHERE registration_year IS NOT NULL
  AND registration_year >= 1800
  AND registration_year <= 2025
GROUP BY registration_year
ORDER BY registration_year ASC;

-- ----------------------------------------------------------------------------
-- 3. Company Registration in the Year 2015 by District
-- ----------------------------------------------------------------------------
SELECT 
    z.district AS district,
    COUNT(c.cin) AS registration_count
FROM company_master c
JOIN zip_code_district z 
    ON c.pin_code = z.pin_code
WHERE c.registration_year = 2015
GROUP BY z.district
ORDER BY registration_count DESC;

-- ----------------------------------------------------------------------------
-- 4. Grouped Registrations: Top 5 Principal Business Activities (2015 - 2025)
-- ----------------------------------------------------------------------------
WITH top_5_activities AS (
    SELECT 'Business Services' AS activity, 1 AS ord
    UNION ALL SELECT 'Agriculture and Allied Activities', 2
    UNION ALL SELECT 'Trading', 3
    UNION ALL SELECT 'Community, personal and Social Services', 4
    UNION ALL SELECT 'Manufacturing (Metals and Chemicals, and products thereof)', 5
)
SELECT 
    c.registration_year AS reg_year,
    c.industrial_classification AS companyindustrialclassification,
    COUNT(*) AS registrations_count
FROM company_master c
JOIN top_5_activities a 
    ON c.industrial_classification = a.activity
WHERE c.registration_year BETWEEN 2015 AND 2025
GROUP BY c.registration_year, c.industrial_classification
ORDER BY c.registration_year ASC, registrations_count DESC;
