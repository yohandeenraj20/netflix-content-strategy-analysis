"""
Netflix Content Analysis - Data Cleaning & EDA
------------------------------------------------
This script:
1. Loads the raw Netflix titles dataset
2. Cleans missing values and inconsistent formats
3. Engineers new features (year_added, month_added, primary_genre, content_age)
4. Runs exploratory analysis and saves charts
5. Exports a cleaned CSV ready for SQL loading / Power BI
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

RAW_PATH = "../data/netflix_titles.csv"
CLEAN_PATH = "../data/netflix_titles_cleaned.csv"
CHART_DIR = "../charts"
os.makedirs(CHART_DIR, exist_ok=True)

# ---------- 1. LOAD ----------
df = pd.read_csv(RAW_PATH)
print(f"Raw shape: {df.shape}")
print("\nMissing values before cleaning:\n", df.isnull().sum())

# ---------- 2. CLEAN ----------
df['director'] = df['director'].fillna('Not Given')
df['country'] = df['country'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Not Given')
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df = df.dropna(subset=['date_added'])

df = df.drop_duplicates(subset=['title', 'release_year'])

# ---------- 3. FEATURE ENGINEERING ----------
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()
df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip())
df['primary_country'] = df['country'].apply(lambda x: x.split(',')[0].strip())
df['content_age_at_add'] = df['year_added'] - df['release_year']
df['content_age_at_add'] = df['content_age_at_add'].clip(lower=0)

df['duration_minutes'] = df.apply(
    lambda r: int(r['duration'].split()[0]) if r['type'] == 'Movie' else None, axis=1
)
df['seasons'] = df.apply(
    lambda r: int(r['duration'].split()[0]) if r['type'] == 'TV Show' else None, axis=1
)

print(f"\nCleaned shape: {df.shape}")

# ---------- 4. EDA ----------
type_counts = df['type'].value_counts()
plt.figure(figsize=(5,5))
type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Content Type Distribution')
plt.ylabel('')
plt.savefig(f'{CHART_DIR}/01_type_distribution.png', bbox_inches='tight', dpi=120)
plt.close()

yearly = df.groupby('year_added').size()
plt.figure(figsize=(8,5))
yearly.plot(kind='line', marker='o')
plt.title('Content Added to Netflix by Year')
plt.xlabel('Year Added')
plt.ylabel('Titles Added')
plt.grid(alpha=0.3)
plt.savefig(f'{CHART_DIR}/02_yearly_growth.png', bbox_inches='tight', dpi=120)
plt.close()

top_countries = df['primary_country'].value_counts().head(10)
plt.figure(figsize=(8,5))
top_countries.sort_values().plot(kind='barh')
plt.title('Top 10 Countries by Content Volume')
plt.xlabel('Number of Titles')
plt.savefig(f'{CHART_DIR}/03_top_countries.png', bbox_inches='tight', dpi=120)
plt.close()

top_genres = df['primary_genre'].value_counts().head(10)
plt.figure(figsize=(8,5))
top_genres.sort_values().plot(kind='barh', color='crimson')
plt.title('Top 10 Genres')
plt.xlabel('Number of Titles')
plt.savefig(f'{CHART_DIR}/04_top_genres.png', bbox_inches='tight', dpi=120)
plt.close()

rating_counts = df['rating'].value_counts()
plt.figure(figsize=(8,5))
rating_counts.plot(kind='bar', color='seagreen')
plt.title('Content Rating Distribution')
plt.ylabel('Number of Titles')
plt.savefig(f'{CHART_DIR}/05_rating_distribution.png', bbox_inches='tight', dpi=120)
plt.close()

print(f"\nCharts saved to {CHART_DIR}/")

# ---------- 5. EXPORT CLEAN DATA ----------
df.to_csv(CLEAN_PATH, index=False)
print(f"\nCleaned dataset exported to {CLEAN_PATH}")

# ---------- 6. QUICK INSIGHT SUMMARY (for README) ----------
print("\n--- KEY INSIGHTS ---")
print(f"Total titles analyzed: {len(df)}")
print(f"Movies vs TV Shows: {type_counts.to_dict()}")
print(f"Top country: {top_countries.index[0]} ({top_countries.iloc[0]} titles)")
print(f"Top genre: {top_genres.index[0]} ({top_genres.iloc[0]} titles)")
print(f"Peak content-addition year: {yearly.idxmax()} ({yearly.max()} titles)")
