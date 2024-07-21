## Analytical Questions
-- 1. How many countries speak French?
SELECT COUNT(1)
FROM public.world_countries as wc
WHERE
    wc.languages LIKE 'French%';
-- 2. How many countries speak English?
SELECT COUNT(1)
FROM public.world_countries as wc
WHERE
    wc.languages LIKE 'English%';
-- 3. How many countries have more than 1 official language?
-- 4. How many countries' official currency is Euro?
-- 5. How many countries are from Western Europe?
-- 6. How many countries have not yet gained independence?
-- 7. How many distinct continents and how many countries from each?
-- 8. How many countries' start of the week is not Monday?
-- 9. How many countries are not United Nation members?
-- 10. How many countries are United Nation members?
-- 11. Least 2 countries with the lowest population for each continent
-- 12. Top 2 countries with the largest area for each continent
-- 13. Top 5 countries with the largest area