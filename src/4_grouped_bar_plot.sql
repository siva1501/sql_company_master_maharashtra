-- Problem 4: Grouped Registrations by Year and Top 5 Business Activities
-- Aggregates registrations over years (2015-2025) for top 5 activities:
-- Business Services, Agriculture, Trading, Community & Social, Manufacturing

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
