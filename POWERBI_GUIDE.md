# Power BI Dashboard Build Guide

Power BI is a desktop app, so this is a step-by-step guide to build the
`.pbix` yourself (takes ~45–60 minutes). Recruiters usually want a
screenshot or a short screen-recording GIF in your README/GitHub — see the
bottom of this file for how to capture that.

## 1. Load the data
1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Load `data/netflix_titles_cleaned.csv` (the file produced by the Python script)
3. Click **Transform Data** to open Power Query and confirm column types:
   - `date_added` → Date
   - `release_year`, `year_added`, `content_age_at_add`, `duration_minutes`, `seasons` → Whole Number

## 2. Create these DAX measures
In the Fields pane, right-click the table → **New Measure**:

```DAX
Total Titles = COUNTROWS(netflix_titles_cleaned)

Total Movies = CALCULATE([Total Titles], netflix_titles_cleaned[type] = "Movie")

Total TV Shows = CALCULATE([Total Titles], netflix_titles_cleaned[type] = "TV Show")

% Movies = DIVIDE([Total Movies], [Total Titles], 0)

Avg Content Age at Add =
AVERAGE(netflix_titles_cleaned[content_age_at_add])

YoY Titles Growth % =
VAR CurrentYear = [Total Titles]
VAR PriorYear =
    CALCULATE(
        [Total Titles],
        FILTER(ALL(netflix_titles_cleaned), netflix_titles_cleaned[year_added] = MAX(netflix_titles_cleaned[year_added]) - 1)
    )
RETURN DIVIDE(CurrentYear - PriorYear, PriorYear, 0)
```

## 3. Build the report page — "Netflix Content Strategy Dashboard"

**Top row — KPI cards:**
- Total Titles
- Total Movies / Total TV Shows
- % Movies
- Avg Content Age at Add

**Row 2 — Trend:**
- Line chart: `year_added` (X-axis) vs `Total Titles` (Y-axis) → shows platform growth

**Row 3 — Composition:**
- Donut chart: `type` → Movie vs TV Show split
- Bar chart: Top 10 `primary_genre` by Total Titles
- Bar chart: Top 10 `primary_country` by Total Titles

**Row 4 — Detail/filter:**
- Table visual: `title`, `type`, `primary_genre`, `primary_country`, `release_year`
- Slicers: `year_added` (slider), `type` (buttons), `rating` (dropdown)

## 4. Formatting tips (this is what separates "fresher project" from "portfolio-ready")
- Use a dark theme (View → Themes → pick a dark one) — matches Netflix's brand
- Add a title text box: "Netflix Content Strategy Dashboard — What is Netflix Investing In?"
- Make all KPI cards the same size, aligned in a row
- Add subtle background color (#141414, Netflix's actual background color) for visual polish
- Turn on tooltips showing extra info (e.g., description) on hover over the country/genre bars

## 5. Capture it for GitHub
1. Once built, go to **File → Export → PDF** (for a static preview) OR
2. Use Windows/Mac screen recording to make a 10–15 second GIF cycling through
   filters (use a tool like ScreenToGif or Giphy Capture)
3. Save the screenshot/GIF into a `screenshots/` folder in your repo
4. Embed it in your README with:
   ```markdown
   ![Dashboard Preview](screenshots/dashboard.png)
   ```

## 6. Publish (optional, but strong for interviews)
If you have a free Power BI account, **Publish to Web** and drop the
public embed link in your README — lets recruiters interact with it
live without opening Power BI.
