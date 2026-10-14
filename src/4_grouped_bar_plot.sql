-- Problem 4: Grouped Registrations by Year and Top 5 Business Activities
-- Aggregates registrations over the last 10 years for the top 5 principal
-- business activities (industrial classifications).

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
