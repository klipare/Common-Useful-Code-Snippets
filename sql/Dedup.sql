-- Deduplicate records from MF_NAV_HISTORY Table
WITH cte AS (
    SELECT 
        scheme_code, 
        date, 
        ROW_NUMBER() OVER (
            PARTITION BY 
                scheme_code, 
                date
            ORDER BY 
                scheme_code, 
                date
        ) row_num
     FROM 
        [HOME].[AMFI].[MF_NAV_HIST]
)
DELETE FROM cte
WHERE row_num > 1;