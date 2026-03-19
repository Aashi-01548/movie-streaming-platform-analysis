"""
STEP 1: Initial Data Exploration
This script helps you understand your dataset structure and contents
"""

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('/mnt/user-data/uploads/MoviesOnStreamingPlatforms_updated.csv')

print("="*60)
print("DATASET OVERVIEW")
print("="*60)

# 1. Basic Information
print(f"\n📊 Total Records: {len(df)}")
print(f"📊 Total Columns: {len(df.columns)}")
print(f"\n📋 Column Names:")
print(df.columns.tolist())

# 2. First few rows
print("\n" + "="*60)
print("SAMPLE DATA (First 5 rows)")
print("="*60)
print(df.head())

# 3. Data types
print("\n" + "="*60)
print("DATA TYPES")
print("="*60)
print(df.dtypes)

# 4. Missing values
print("\n" + "="*60)
print("MISSING VALUES")
print("="*60)
missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_percent
})
print(missing_df[missing_df['Missing Count'] > 0])

# 5. Platform distribution
print("\n" + "="*60)
print("MOVIES PER PLATFORM")
print("="*60)
platforms = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
for platform in platforms:
    count = df[platform].sum()
    percentage = (count / len(df)) * 100
    print(f"{platform}: {count} movies ({percentage:.2f}%)")

# 6. Basic statistics
print("\n" + "="*60)
print("BASIC STATISTICS")
print("="*60)
print(df.describe())

print("\n✅ Exploration Complete!")
print("Next step: Data Cleaning")
