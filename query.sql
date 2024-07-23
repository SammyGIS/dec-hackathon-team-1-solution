## Analytical Questions

-- 1. How many countries speak French?
SELECT COUNT(*) FROM world_countries 
WHERE languages LIKE '%French%';

-- 2. How many countries speak English?
SELECT COUNT(*) FROM world_countries 
WHERE languages LIKE '%English%';

-- 3. How many countries have more than 1 official language?
SELECT COUNT(*) FROM world_countries 
WHERE LENGTH(languages) - LENGTH(REPLACE(languages, ',', '')) + 1 > 1;

-- 4. How many countries' official currency is Euro?
SELECT COUNT(*) FROM world_countries 
WHERE currency_code = 'EUR';

-- 5. How many countries are from Western Europe?
SELECT COUNT(*) FROM world_countries 
WHERE sub_region = 'Western Europe';

-- 6. How many countries have not yet gained independence?
SELECT COUNT(*) FROM world_countries 
WHERE independence = FALSE;

-- 7. How many distinct continents and how many countries from each?
SELECT continents, COUNT(*) AS country_count FROM world_countries 
GROUP BY continents;

-- 8. How many countries' start of the week is not Monday?
SELECT COUNT(*) FROM world_countries 
WHERE start_of_week <> 'Monday';

-- 9. How many countries are not United Nation members?
SELECT COUNT(*) FROM world_countries 
WHERE un_members = FALSE;

-- 10. How many countries are United Nation members?
SELECT COUNT(*) FROM world_countries 
WHERE un_members = TRUE;

-- 11. Least 2 countries with the lowest population for each continent
WITH RankedCountries AS (
    SELECT continents, country_name, population,
           ROW_NUMBER() OVER (PARTITION BY continents ORDER BY population ASC) AS rank
    FROM world_countries
)
SELECT continents, country_name, population
FROM RankedCountries
WHERE rank <= 2;


-- 12. Top 2 countries with the largest area for each continent
WITH RankedCountries AS (
    SELECT continents, country_name, area,
           ROW_NUMBER() OVER (PARTITION BY continents ORDER BY area DESC) AS rank
    FROM world_countries
)
SELECT continents, country_name, area
FROM RankedCountries
WHERE rank <= 2;

-- 13. Top 5 countries with the largest area
SELECT country_name, area FROM world_countries 
ORDER BY area DESC LIMIT 5;

-- 14. Top 5 countries with the lowest area
SELECT country_name, area FROM world_countries 
ORDER BY area ASC LIMIT 5;