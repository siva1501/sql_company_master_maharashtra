-- Problem 2: Company Registrations by Year
-- Extracts the registration year from registration date and counts companies per year

SELECT 
    registration_year AS year,
    COUNT(*) AS count
FROM company_master
WHERE registration_year IS NOT NULL
  AND registration_year >= 1900
  AND registration_year <= 2026
GROUP BY registration_year
ORDER BY registration_year ASC;
