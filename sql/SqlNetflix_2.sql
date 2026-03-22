-- ============================================================
-- NETFLIX CONTENT ANALYSIS PROJECT
-- Step 2: Analytical SQL Queries
-- ============================================================

USE netflix_db;

-- -------------------------------------------------------
-- QUERY 1: Content Type Distribution (Movies vs TV Shows)
-- -------------------------------------------------------
SELECT 
    type,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) AS percentage
FROM netflix_titles
GROUP BY type
ORDER BY count DESC;

-- -------------------------------------------------------
-- QUERY 2: Top 10 Countries by Content Volume
-- -------------------------------------------------------
SELECT 
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(country, ',', n.n), ',', -1)) AS single_country,
    COUNT(*) AS content_count
FROM netflix_titles
JOIN (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
) n ON CHAR_LENGTH(country) - CHAR_LENGTH(REPLACE(country, ',', '')) >= n.n - 1
WHERE country IS NOT NULL AND country != ''
GROUP BY single_country
ORDER BY content_count DESC
LIMIT 10;

-- -------------------------------------------------------
-- QUERY 3: Content Added Per Year (Growth Trend)
-- -------------------------------------------------------
SELECT 
    SUBSTRING_INDEX(TRIM(date_added), ' ', -1) AS year_added,
    COUNT(*) AS titles_added,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movies_added,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS shows_added
FROM netflix_titles
WHERE date_added IS NOT NULL AND date_added != ''
GROUP BY year_added
HAVING year_added REGEXP '^[0-9]{4}$'
ORDER BY year_added;

-- -------------------------------------------------------
-- QUERY 4: Rating Distribution (Content Maturity Levels)
-- -------------------------------------------------------
SELECT 
    rating,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles WHERE rating IS NOT NULL AND rating != ''), 2) AS percentage
FROM netflix_titles
WHERE rating IS NOT NULL AND rating != ''
GROUP BY rating
ORDER BY count DESC;

-- -------------------------------------------------------
-- QUERY 5: Top 10 Most Common Genres
-- -------------------------------------------------------
SELECT 
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(listed_in, ',', n.n), ',', -1)) AS genre,
    COUNT(*) AS count
FROM netflix_titles
JOIN (
    SELECT 1 n UNION SELECT 2 UNION SELECT 3
) n ON CHAR_LENGTH(listed_in) - CHAR_LENGTH(REPLACE(listed_in, ',', '')) >= n.n - 1
WHERE listed_in IS NOT NULL
GROUP BY genre
ORDER BY count DESC
LIMIT 10;

-- -------------------------------------------------------
-- QUERY 6: Most Prolific Directors (Top 10)
-- -------------------------------------------------------
SELECT 
    director,
    COUNT(*) AS titles,
    GROUP_CONCAT(DISTINCT type ORDER BY type SEPARATOR ', ') AS content_types
FROM netflix_titles
WHERE director IS NOT NULL AND director != ''
GROUP BY director
ORDER BY titles DESC
LIMIT 10;

-- -------------------------------------------------------
-- QUERY 7: Average Movie Duration by Rating
-- -------------------------------------------------------
SELECT 
    rating,
    AVG(CAST(REPLACE(duration, ' min', '') AS UNSIGNED)) AS avg_duration_minutes,
    COUNT(*) AS movie_count
FROM netflix_titles
WHERE type = 'Movie' 
  AND duration LIKE '%min%'
  AND rating IS NOT NULL AND rating != ''
GROUP BY rating
ORDER BY avg_duration_minutes DESC;

-- -------------------------------------------------------
-- QUERY 8: Content Released Decade Analysis
-- -------------------------------------------------------
SELECT 
    CONCAT(FLOOR(release_year / 10) * 10, 's') AS decade,
    COUNT(*) AS total_titles,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movies,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows
FROM netflix_titles
WHERE release_year IS NOT NULL
GROUP BY decade
ORDER BY decade;

-- -------------------------------------------------------
-- QUERY 9: TV Show Season Distribution
-- -------------------------------------------------------
SELECT 
    duration AS seasons,
    COUNT(*) AS show_count
FROM netflix_titles
WHERE type = 'TV Show' AND duration IS NOT NULL
GROUP BY duration
ORDER BY show_count DESC
LIMIT 10;

-- -------------------------------------------------------
-- QUERY 10: US Content Strategy Over Time
-- -------------------------------------------------------
SELECT 
    SUBSTRING_INDEX(TRIM(date_added), ' ', -1) AS year_added,
    COUNT(*) AS us_titles,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS us_movies,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS us_shows
FROM netflix_titles
WHERE country LIKE '%United States%'
  AND date_added IS NOT NULL AND date_added != ''
GROUP BY year_added
HAVING year_added REGEXP '^[0-9]{4}$'
ORDER BY year_added;

-- -------------------------------------------------------
-- EXPORT CLEAN DATA FOR PYTHON
-- -------------------------------------------------------
SELECT 
    show_id, type, title, director, cast_members,
    country, date_added, release_year, rating, duration,
    listed_in, description
FROM netflix_titles
INTO OUTFILE '/var/lib/mysql-files/netflix_clean_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
