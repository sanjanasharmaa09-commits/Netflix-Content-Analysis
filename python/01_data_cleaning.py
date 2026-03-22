"""
NETFLIX CONTENT ANALYSIS PROJECT
Step 3: Data Cleaning & Preprocessing
File: 01_data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

# ── Load Dataset 
# Download from: https://www.kaggle.com/datasets/shivamb/netflix-shows
df = pd.read_csv('data/netflix_titles.csv')

print("=" * 60)
print("NETFLIX DATA CLEANING REPORT")
print("=" * 60)
print(f"\nOriginal Shape: {df.shape}")
print(f"\nColumn Names:\n{df.columns.tolist()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nMissing % :\n{round(df.isnull().sum() / len(df) * 100, 2)}")

# ── Step 1: Remove Duplicates
before = len(df)
df.drop_duplicates(subset='show_id', inplace=True)
print(f"\n[1] Duplicates removed: {before - len(df)}")

# ── Step 2: Fill Missing Values 
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['rating'].fillna('Not Rated', inplace=True)
df['date_added'].fillna('Unknown', inplace=True)
df.dropna(subset=['duration'], inplace=True)   # Very few missing – drop them
print(f"[2] Missing values filled. Shape: {df.shape}")

# ── Step 3: Clean & Parse date_added 
df['date_added'] = df['date_added'].str.strip()
df['date_added_clean'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added']  = df['date_added_clean'].dt.year.astype('Int64')
df['month_added'] = df['date_added_clean'].dt.month.astype('Int64')
df['month_name']  = df['date_added_clean'].dt.strftime('%B')
print("[3] Date columns parsed.")

# ── Step 4: Extract Duration Numbers 
def extract_duration(row):
    try:
        if row['type'] == 'Movie':
            return int(row['duration'].replace(' min', '').strip())
        else:  # TV Show
            return int(row['duration'].replace(' Season', '').replace(' Seasons', '').strip())
    except:
        return np.nan

df['duration_value'] = df.apply(extract_duration, axis=1)
print("[4] Duration values extracted.")

# ── Step 5: Split Listed_in Into Primary Genre 
df['primary_genre'] = df['listed_in'].apply(
    lambda x: x.split(',')[0].strip() if pd.notna(x) else 'Unknown'
)

# ── Step 6: Primary Country 
df['primary_country'] = df['country'].apply(
    lambda x: x.split(',')[0].strip() if pd.notna(x) else 'Unknown'
)

# ── Step 7: Content Age (years since release) 
df['content_age'] = 2024 - df['release_year']

# ── Step 8: Encode Type as Binary (for ML) 
df['type_encoded'] = (df['type'] == 'Movie').astype(int)   # 1=Movie, 0=TV Show

# ── Step 9: Clean Title 
df['title'] = df['title'].str.strip()

# ── Final Report 
print(f"\n[5] Final cleaned shape: {df.shape}")
print(f"\nMissing after clean:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# ── Save Clean Dataset
os.makedirs('data', exist_ok=True)
df.to_csv('data/netflix_cleaned.csv', index=False)
print("\n✅ Cleaned dataset saved → data/netflix_cleaned.csv")
print(f"   Rows: {len(df):,}  |  Columns: {len(df.columns)}")
