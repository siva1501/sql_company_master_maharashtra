-- Problem 3: Company Registrations in 2015 by District
-- Filters for registration year 2015, joins with the zip_code_district table
-- via the 6-digit postal code extracted from the address,
-- and aggregates counts by district in descending order.

SELECT 
    z.district AS district,
    COUNT(c.cin) AS count
FROM company_master c
JOIN zip_code_district z 
    ON c.pin_code = z.pin_code
WHERE c.registration_year = 2015
GROUP BY z.district
ORDER BY count DESC;
