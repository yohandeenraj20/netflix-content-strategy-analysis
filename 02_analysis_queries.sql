-- =========================================================
-- Netflix Content Analysis - Business Question Queries
-- These are the queries to screenshot / discuss in interviews.
-- Each one answers a real business question, not just "SELECT *".
-- =========================================================

-- Q1. What is the yearly trend of content added to the platform?
SELECT
    year_added,
    COUNT(*) AS titles_added
FROM netflix_titles
GROUP BY year_added
ORDER BY year_added;


-- Q2. Movies vs TV Shows split, with percentage of total
SELECT
    type,
    COUNT(*) AS total_titles,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM netflix_titles
GROUP BY type;


-- Q3. Top 10 countries by content volume
SELECT
    primary_country,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY primary_country
ORDER BY total_titles DESC
LIMIT 10;


-- Q4. Top 5 genres per content type (Movie / TV Show) using window function
WITH genre_counts AS (
    SELECT
        type,
        primary_genre,
        COUNT(*) AS total_titles,
        RANK() OVER (PARTITION BY type ORDER BY COUNT(*) DESC) AS genre_rank
    FROM netflix_titles
    GROUP BY type, primary_genre
)
SELECT type, primary_genre, total_titles
FROM genre_counts
WHERE genre_rank <= 5
ORDER BY type, genre_rank;


-- Q5. Average "content age" at the time it was added (freshness of catalog)
-- i.e. how many years after release did Netflix add the title?
SELECT
    type,
    ROUND(AVG(content_age_at_add), 1) AS avg_years_after_release
FROM netflix_titles
GROUP BY type;


-- Q6. Which directors have the most titles on the platform? (Top 10)
SELECT
    director,
    COUNT(*) AS total_titles
FROM netflix_titles
WHERE director <> 'Not Given'
GROUP BY director
ORDER BY total_titles DESC
LIMIT 10;


-- Q7. Month-over-month seasonality: which months does Netflix add the most content?
SELECT
    month_added,
    COUNT(*) AS titles_added
FROM netflix_titles
GROUP BY month_added
ORDER BY titles_added DESC;


-- Q8. Running (cumulative) total of titles added over the years
SELECT
    year_added,
    COUNT(*) AS titles_added,
    SUM(COUNT(*)) OVER (ORDER BY year_added) AS cumulative_titles
FROM netflix_titles
GROUP BY year_added
ORDER BY year_added;


-- Q9. Content rating distribution by type (maturity mix)
SELECT
    type,
    rating,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY type, rating
ORDER BY type, total_titles DESC;


-- Q10. Year-over-year % growth in titles added
WITH yearly AS (
    SELECT year_added, COUNT(*) AS titles_added
    FROM netflix_titles
    GROUP BY year_added
)
SELECT
    year_added,
    titles_added,
    LAG(titles_added) OVER (ORDER BY year_added) AS prev_year_titles,
    ROUND(
        100.0 * (titles_added - LAG(titles_added) OVER (ORDER BY year_added))
        / NULLIF(LAG(titles_added) OVER (ORDER BY year_added), 0), 2
    ) AS pct_growth
FROM yearly
ORDER BY year_added;
