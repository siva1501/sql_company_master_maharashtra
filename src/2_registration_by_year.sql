-- Problem 2: Company Registrations by Year
-- Extracts the registration year and counts companies chronologically

SELECT 
    registration_year,
    COUNT(*) AS company_count
FROM company_master
WHERE registration_year IS NOT NULL
  AND registration_year >= 1800
  AND registration_year <= 2025
GROUP BY registration_year
ORDER BY registration_year ASC;
