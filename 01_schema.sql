-- =========================================================
-- Netflix Content Analysis - Schema
-- Compatible with PostgreSQL / MySQL (minor tweaks for SQL Server)
-- =========================================================

DROP TABLE IF EXISTS netflix_titles;

CREATE TABLE netflix_titles (
    show_id         VARCHAR(10) PRIMARY KEY,
    type            VARCHAR(20)  NOT NULL,      -- 'Movie' or 'TV Show'
    title           VARCHAR(255) NOT NULL,
    director        VARCHAR(255),
    cast_members    TEXT,
    country         VARCHAR(255),
    date_added      DATE,
    release_year    INT,
    rating          VARCHAR(10),
    duration        VARCHAR(20),
    listed_in       TEXT,                       -- genres, comma separated
    description     TEXT,
    year_added      INT,
    month_added     VARCHAR(20),
    primary_genre   VARCHAR(100),
    primary_country VARCHAR(100),
    content_age_at_add INT,
    duration_minutes INT,
    seasons         INT
);

-- Load the cleaned CSV (adjust path/COPY syntax to your DB engine)
-- PostgreSQL example:
-- COPY netflix_titles FROM '/path/to/netflix_titles_cleaned.csv' DELIMITER ',' CSV HEADER;

-- MySQL example:
-- LOAD DATA INFILE '/path/to/netflix_titles_cleaned.csv'
-- INTO TABLE netflix_titles
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
