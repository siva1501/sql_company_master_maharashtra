-- ============================================================================
-- All Analytical Queries: Company Master - Maharashtra
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Histogram of Authorized Capital
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN authorized_capital <= 100000 THEN '<= 1L'
        WHEN authorized_capital <= 1000000 THEN '1L to 10L'
        WHEN authorized_capital <= 10000000 THEN '10L to 1Cr'
        WHEN authorized_capital <= 100000000 THEN '1Cr to 10Cr'
        ELSE '> 10Cr'
    END AS capital_range,
    COUNT(*) AS count
FROM company_master
WHERE authorized_capital IS NOT NULL
GROUP BY capital_range
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
    registration_year AS year,
    COUNT(*) AS count
FROM company_master
WHERE registration_year IS NOT NULL
  AND registration_year >= 1900
  AND registration_year <= 2026
GROUP BY registration_year
ORDER BY registration_year ASC;

-- ----------------------------------------------------------------------------
-- 3. Company Registration in the Year 2015 by District
-- ----------------------------------------------------------------------------
SELECT 
    z.district AS district,
    COUNT(c.cin) AS count
FROM company_master c
JOIN zip_code_district z 
    ON c.pin_code = z.pin_code
WHERE c.registration_year = 2015
GROUP BY z.district
ORDER BY count DESC;

-- ----------------------------------------------------------------------------
-- 4. Grouped Registrations: Top 5 Principal Business Activities (Last 10 Years)
-- ----------------------------------------------------------------------------
WITH last_10_years AS (
    SELECT DISTINCT registration_year
    FROM company_master
    WHERE registration_year IS NOT NULL 
      AND registration_year BETWEEN 1900 AND 2026
    ORDER BY registration_year DESC
    LIMIT 10
),
top_5_activities AS (
    SELECT 
        c.industrial_classification AS activity,
        COUNT(*) AS total_count
    FROM company_master c
    JOIN last_10_years y ON c.registration_year = y.registration_year
    WHERE c.industrial_classification IS NOT NULL 
      AND c.industrial_classification != ''
    GROUP BY c.industrial_classification
    ORDER BY total_count DESC
    LIMIT 5
)
SELECT 
    c.registration_year AS year,
    c.industrial_classification AS activity,
    COUNT(*) AS count
FROM company_master c
JOIN last_10_years y ON c.registration_year = y.registration_year
JOIN top_5_activities a ON c.industrial_classification = a.activity
GROUP BY c.registration_year, c.industrial_classification
ORDER BY c.registration_year ASC, a.total_count DESC;
