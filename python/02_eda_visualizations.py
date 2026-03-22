"""
NETFLIX CONTENT ANALYSIS PROJECT
Step 4: Exploratory Data Analysis & Visualizations
File: 02_eda_visualizations.py

Run AFTER 01_data_cleaning.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# ── Settings ──────────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid")
NETFLIX_RED  = '#E50914'
NETFLIX_DARK = '#141414'
NETFLIX_GRAY = '#564d4d'
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'DejaVu Sans'

os.makedirs('outputs/charts', exist_ok=True)

# ── Load Cleaned Data ─────────────────────────────────────────────────────────
df = pd.read_csv('data/netflix_cleaned.csv')
print(f"Loaded {len(df):,} records\n")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 1: Content Type Distribution (Pie)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

type_counts = df['type'].value_counts()
colors = [NETFLIX_RED, '#831010']
wedges, texts, autotexts = ax.pie(
    type_counts, labels=type_counts.index,
    autopct='%1.1f%%', colors=colors,
    startangle=90, textprops={'color': 'white', 'fontsize': 13}
)
for at in autotexts:
    at.set_fontsize(14); at.set_fontweight('bold')

ax.set_title('Netflix Content: Movies vs TV Shows', color='white',
             fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('outputs/charts/01_content_type_pie.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 1 saved: Content Type Distribution")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 2: Content Added Per Year (Line)
# ─────────────────────────────────────────────────────────────────────────────
yearly = df.groupby(['year_added', 'type']).size().reset_index(name='count')
yearly = yearly[yearly['year_added'].between(2008, 2021)]

fig, ax = plt.subplots(figsize=(12, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

for ctype, color in [('Movie', NETFLIX_RED), ('TV Show', '#FFA500')]:
    data = yearly[yearly['type'] == ctype]
    ax.plot(data['year_added'], data['count'], marker='o', linewidth=2.5,
            color=color, label=ctype, markersize=6)

ax.set_title('Netflix Content Growth Over Years', color='white', fontsize=16, fontweight='bold')
ax.set_xlabel('Year', color='white', fontsize=12)
ax.set_ylabel('Titles Added', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.legend(facecolor=NETFLIX_GRAY, labelcolor='white', fontsize=11)
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/charts/02_content_growth_yearly.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 2 saved: Content Growth Over Years")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 3: Top 10 Countries (Horizontal Bar)
# ─────────────────────────────────────────────────────────────────────────────
top_countries = df['primary_country'].value_counts().head(11)
top_countries = top_countries[top_countries.index != 'Unknown'].head(10)

fig, ax = plt.subplots(figsize=(10, 7), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

bars = ax.barh(top_countries.index[::-1], top_countries.values[::-1],
               color=NETFLIX_RED, edgecolor='none')

for bar, val in zip(bars, top_countries.values[::-1]):
    ax.text(val + 30, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', ha='left', color='white', fontsize=10)

ax.set_title('Top 10 Countries by Netflix Content', color='white', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Titles', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/charts/03_top_countries.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 3 saved: Top Countries")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4: Rating Distribution (Bar)
# ─────────────────────────────────────────────────────────────────────────────
rating_order = ['G','TV-Y','TV-Y7','TV-Y7-FV','PG','TV-G','TV-PG','PG-13','TV-14','R','TV-MA','NC-17','NR','UR','Not Rated']
ratings = df['rating'].value_counts()
ratings = ratings[[r for r in rating_order if r in ratings.index]]

fig, ax = plt.subplots(figsize=(12, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

palette = sns.color_palette("YlOrRd", len(ratings))
bars = ax.bar(ratings.index, ratings.values, color=palette, edgecolor='none')

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
            f'{int(bar.get_height()):,}', ha='center', va='bottom',
            color='white', fontsize=8)

ax.set_title('Content Rating Distribution on Netflix', color='white', fontsize=16, fontweight='bold')
ax.set_xlabel('Rating', color='white', fontsize=12)
ax.set_ylabel('Number of Titles', color='white', fontsize=12)
ax.tick_params(colors='white', rotation=30)
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/charts/04_rating_distribution.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 4 saved: Rating Distribution")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5: Top 10 Genres (Bar)
# ─────────────────────────────────────────────────────────────────────────────
genres = df['primary_genre'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

colors_gen = [NETFLIX_RED if i == 0 else '#831010' for i in range(len(genres))]
bars = ax.bar(genres.index, genres.values, color=colors_gen, edgecolor='none')

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            f'{int(bar.get_height()):,}', ha='center', va='bottom',
            color='white', fontsize=9)

ax.set_title('Top 10 Genres on Netflix', color='white', fontsize=16, fontweight='bold')
ax.set_xlabel('Genre', color='white', fontsize=12)
ax.set_ylabel('Number of Titles', color='white', fontsize=12)
ax.tick_params(colors='white', axis='x', rotation=20)
ax.tick_params(colors='white', axis='y')
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/charts/05_top_genres.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 5 saved: Top Genres")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 6: Movie Duration Distribution (Histogram)
# ─────────────────────────────────────────────────────────────────────────────
movies = df[(df['type'] == 'Movie') & df['duration_value'].notna()]
movies = movies[movies['duration_value'].between(10, 300)]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

ax.hist(movies['duration_value'], bins=40, color=NETFLIX_RED, edgecolor='black', alpha=0.85)
ax.axvline(movies['duration_value'].mean(), color='white', linestyle='--', linewidth=2,
           label=f"Mean: {movies['duration_value'].mean():.0f} min")
ax.axvline(movies['duration_value'].median(), color='#FFA500', linestyle='--', linewidth=2,
           label=f"Median: {movies['duration_value'].median():.0f} min")

ax.set_title('Distribution of Movie Durations', color='white', fontsize=16, fontweight='bold')
ax.set_xlabel('Duration (minutes)', color='white', fontsize=12)
ax.set_ylabel('Frequency', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.legend(facecolor=NETFLIX_GRAY, labelcolor='white', fontsize=11)
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/charts/06_movie_duration_hist.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 6 saved: Movie Duration Distribution")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 7: Monthly Content Addition Heatmap
# ─────────────────────────────────────────────────────────────────────────────
monthly = df.groupby(['year_added', 'month_added']).size().reset_index(name='count')
monthly = monthly[monthly['year_added'].between(2015, 2021)]
heatmap_data = monthly.pivot(index='year_added', columns='month_added', values='count').fillna(0)

month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
heatmap_data.columns = [month_labels[int(m)-1] for m in heatmap_data.columns]

fig, ax = plt.subplots(figsize=(14, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='.0f',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Titles Added'})

ax.set_title('Monthly Content Addition Heatmap (2015–2021)', color='white',
             fontsize=15, fontweight='bold')
ax.set_xlabel('Month', color='white', fontsize=12)
ax.set_ylabel('Year', color='white', fontsize=12)
ax.tick_params(colors='white')

plt.tight_layout()
plt.savefig('outputs/charts/07_monthly_heatmap.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 7 saved: Monthly Heatmap")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 8: TV Show Season Distribution
# ─────────────────────────────────────────────────────────────────────────────
shows = df[df['type'] == 'TV Show']
season_counts = shows['duration_value'].value_counts().sort_index().head(10)

fig, ax = plt.subplots(figsize=(10, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

bars = ax.bar([f"{int(s)} Season{'s' if s>1 else ''}" for s in season_counts.index],
              season_counts.values, color=NETFLIX_RED, edgecolor='none')

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{int(bar.get_height()):,}', ha='center', va='bottom',
            color='white', fontsize=10)

ax.set_title('TV Show Season Count Distribution', color='white', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Seasons', color='white', fontsize=12)
ax.set_ylabel('Number of Shows', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/charts/08_tv_seasons.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Chart 8 saved: TV Show Seasons")

print("\n🎉 All 8 charts saved to outputs/charts/")
