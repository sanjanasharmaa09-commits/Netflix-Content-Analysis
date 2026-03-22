-- ============================================================
-- NETFLIX CONTENT ANALYSIS PROJECT
-- Step 1: Database Setup
-- ============================================================

CREATE DATABASE IF NOT EXISTS netflix_db;
USE netflix_db;

-- Drop table if exists (for re-runs)
DROP TABLE IF EXISTS netflix_titles;

-- Create main table
CREATE TABLE netflix_titles (
    show_id       VARCHAR(10)   PRIMARY KEY,
    type          VARCHAR(10),
    title         VARCHAR(300),
    director      VARCHAR(300),
    cast_members  TEXT,
    country       VARCHAR(200),
    date_added    VARCHAR(50),
    release_year  INT,
    rating        VARCHAR(20),
    duration      VARCHAR(20),
    listed_in     VARCHAR(300),
    description   TEXT
);

-- ============================================================
-- IMPORT DATA (run after placing CSV in MySQL secure-file-priv path)
-- ============================================================
-- Check your secure path: SHOW VARIABLES LIKE 'secure_file_priv';
-- Then copy netflix_titles.csv to that folder and run:

LOAD DATA INFILE '/var/lib/mysql-files/netflix_titles.csv'
INTO TABLE netflix_titles
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(show_id, type, title, director, cast_members, country,
 date_added, release_year, rating, duration, listed_in, description);

-- Verify import
SELECT COUNT(*) AS total_records FROM netflix_titles;
SELECT * FROM netflix_titles LIMIT 5;
