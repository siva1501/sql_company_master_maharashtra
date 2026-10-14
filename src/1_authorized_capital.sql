-- Problem 1: Histogram of Authorized Capital
-- Aggregates company counts into the 5 authorized capital intervals:
--   <= 1L       (<= 100,000)
--   1L to 10L   (100,001 to 1,000,000)
--   10L to 1Cr  (1,000,001 to 10,000,000)
--   1Cr to 10Cr (10,000,001 to 100,000,000)
--   > 10Cr      (> 100,000,000)

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
