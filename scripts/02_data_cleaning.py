"""
STEP 2: Data Cleaning
This script cleans the dataset and prepares it for analysis
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('/mnt/user-data/uploads/MoviesOnStreamingPlatforms_updated.csv')

print("\n" + "="*60)
print("STARTING DATA CLEANING")
print("="*60)

# 1. Handle Rotten Tomatoes column (remove % and convert to numeric)
print("\n1️⃣ Cleaning Rotten Tomatoes scores...")
df['Rotten Tomatoes'] = df['Rotten Tomatoes'].str.replace('%', '')
df['Rotten Tomatoes'] = pd.to_numeric(df['Rotten Tomatoes'], errors='coerce')
print(f"   ✓ Converted to numeric (0-100 scale)")

# 2. Fill missing IMDb ratings with median
print("\n2️⃣ Handling missing IMDb ratings...")
median_imdb = df['IMDb'].median()
df['IMDb'].fillna(median_imdb, inplace=True)
print(f"   ✓ Filled {571} missing values with median: {median_imdb}")

# 3. Fill missing Rotten Tomatoes with median
print("\n3️⃣ Handling missing Rotten Tomatoes scores...")
median_rt = df['Rotten Tomatoes'].median()
df['Rotten Tomatoes'].fillna(median_rt, inplace=True)
print(f"   ✓ Filled missing values with median: {median_rt}")

# 4. Fill missing Age ratings
print("\n4️⃣ Handling missing Age ratings...")
df['Age'].fillna('Not Rated', inplace=True)
print(f"   ✓ Filled missing Age ratings with 'Not Rated'")

# 5. Fill missing Runtime with median
print("\n5️⃣ Handling missing Runtime values...")
median_runtime = df['Runtime'].median()
df['Runtime'].fillna(median_runtime, inplace=True)
print(f"   ✓ Filled missing values with median: {median_runtime} minutes")

# 6. Fill missing Directors, Genres, Country, Language
print("\n6️⃣ Handling other missing values...")
df['Directors'].fillna('Unknown', inplace=True)
df['Genres'].fillna('Unknown', inplace=True)
df['Country'].fillna('Unknown', inplace=True)
df['Language'].fillna('Unknown', inplace=True)
print(f"   ✓ Filled missing text fields with 'Unknown'")

# 7. Fix Netflix column (has .01 values, should be 0 or 1)
print("\n7️⃣ Fixing Netflix column...")
df['Netflix'] = df['Netflix'].round().astype(int)
print(f"   ✓ Converted to binary (0 or 1)")

# 8. Create new useful columns
print("\n8️⃣ Creating new features...")

# Average rating (combining IMDb and Rotten Tomatoes)
# Normalize IMDb to 100 scale: IMDb * 10
df['Average_Rating'] = ((df['IMDb'] * 10) + df['Rotten Tomatoes']) / 2

# Platform count (how many platforms has this movie)
df['Platform_Count'] = df['Netflix'] + df['Hulu'] + df['Prime Video'] + df['Disney+']

# Decade
df['Decade'] = (df['Year'] // 10) * 10

# Runtime category
def categorize_runtime(runtime):
    if runtime < 90:
        return 'Short'
    elif runtime <= 120:
        return 'Medium'
    else:
        return 'Long'

df['Runtime_Category'] = df['Runtime'].apply(categorize_runtime)

# Rating category
def categorize_rating(rating):
    if rating >= 80:
        return 'Excellent'
    elif rating >= 60:
        return 'Good'
    elif rating >= 40:
        return 'Average'
    else:
        return 'Poor'

df['Rating_Category'] = df['Average_Rating'].apply(categorize_rating)

print(f"   ✓ Created 5 new features:")
print(f"      - Average_Rating (combined IMDb & RT)")
print(f"      - Platform_Count (multi-platform availability)")
print(f"      - Decade")
print(f"      - Runtime_Category")
print(f"      - Rating_Category")

# 9. Remove duplicates
print("\n9️⃣ Checking for duplicates...")
duplicates = df.duplicated(subset='Title').sum()
df = df.drop_duplicates(subset='Title', keep='first')
print(f"   ✓ Removed {duplicates} duplicate movies")

# 10. Save cleaned dataset
print("\n🔟 Saving cleaned dataset...")
df.to_csv('/home/claude/streaming_data_clean.csv', index=False)
print(f"   ✓ Saved to: streaming_data_clean.csv")

# Summary
print("\n" + "="*60)
print("CLEANING SUMMARY")
print("="*60)
print(f"Original records: 16,744")
print(f"Final records: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Missing values remaining: {df.isnull().sum().sum()}")

print("\n✅ Data Cleaning Complete!")
print("Next step: Exploratory Data Analysis (EDA)")
