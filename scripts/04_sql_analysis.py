"""
STEP 4: SQL Analysis
This script loads data into SQLite and runs analytical queries
"""

import sqlite3
import pandas as pd

# Load cleaned data
df = pd.read_csv('/home/claude/streaming_data_clean.csv')

print("="*60)
print("SQL DATABASE SETUP & ANALYSIS")
print("="*60)

# Connect to SQLite database
conn = sqlite3.connect('/home/claude/streaming_analytics.db')
cursor = conn.cursor()

# Load data into SQL
print("\n📥 Loading data into SQL database...")
df.to_sql('movies', conn, if_exists='replace', index=False)
print(f"   ✓ Loaded {len(df)} records into 'movies' table")

print("\n" + "="*60)
print("RUNNING SQL QUERIES")
print("="*60)

# Query 1: Platform Content Overview
print("\n1️⃣ PLATFORM CONTENT OVERVIEW")
print("-" * 60)
query1 = """
SELECT 
    'Netflix' as Platform,
    SUM(Netflix) as Total_Movies,
    ROUND(AVG(CASE WHEN Netflix = 1 THEN Average_Rating END), 2) as Avg_Rating,
    ROUND(AVG(CASE WHEN Netflix = 1 THEN Runtime END), 0) as Avg_Runtime
FROM movies
UNION ALL
SELECT 
    'Hulu' as Platform,
    SUM(Hulu) as Total_Movies,
    ROUND(AVG(CASE WHEN Hulu = 1 THEN Average_Rating END), 2) as Avg_Rating,
    ROUND(AVG(CASE WHEN Hulu = 1 THEN Runtime END), 0) as Avg_Runtime
FROM movies
UNION ALL
SELECT 
    'Prime Video' as Platform,
    SUM("Prime Video") as Total_Movies,
    ROUND(AVG(CASE WHEN "Prime Video" = 1 THEN Average_Rating END), 2) as Avg_Rating,
    ROUND(AVG(CASE WHEN "Prime Video" = 1 THEN Runtime END), 0) as Avg_Runtime
FROM movies
UNION ALL
SELECT 
    'Disney+' as Platform,
    SUM("Disney+") as Total_Movies,
    ROUND(AVG(CASE WHEN "Disney+" = 1 THEN Average_Rating END), 2) as Avg_Rating,
    ROUND(AVG(CASE WHEN "Disney+" = 1 THEN Runtime END), 0) as Avg_Runtime
FROM movies
ORDER BY Total_Movies DESC;
"""
result1 = pd.read_sql_query(query1, conn)
print(result1.to_string(index=False))

# Query 2: Top Rated Content per Platform
print("\n\n2️⃣ TOP 5 HIGHEST RATED MOVIES PER PLATFORM")
print("-" * 60)
print("\n🔴 NETFLIX TOP 5:")
query2a = """
SELECT Title, Year, IMDb, "Rotten Tomatoes", Average_Rating, Runtime
FROM movies
WHERE Netflix = 1
ORDER BY Average_Rating DESC
LIMIT 5;
"""
result2a = pd.read_sql_query(query2a, conn)
print(result2a.to_string(index=False))

print("\n🟢 HULU TOP 5:")
query2b = """
SELECT Title, Year, IMDb, "Rotten Tomatoes", Average_Rating, Runtime
FROM movies
WHERE Hulu = 1
ORDER BY Average_Rating DESC
LIMIT 5;
"""
result2b = pd.read_sql_query(query2b, conn)
print(result2b.to_string(index=False))

# Query 3: Content Strategy Analysis
print("\n\n3️⃣ CONTENT STRATEGY INSIGHTS")
print("-" * 60)
query3 = """
SELECT 
    Rating_Category,
    COUNT(*) as Movie_Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM movies), 2) as Percentage,
    ROUND(AVG(Average_Rating), 2) as Avg_Rating,
    ROUND(AVG(Platform_Count), 2) as Avg_Platforms
FROM movies
GROUP BY Rating_Category
ORDER BY 
    CASE Rating_Category
        WHEN 'Excellent' THEN 1
        WHEN 'Good' THEN 2
        WHEN 'Average' THEN 3
        WHEN 'Poor' THEN 4
    END;
"""
result3 = pd.read_sql_query(query3, conn)
print(result3.to_string(index=False))

# Query 4: Decade-wise Performance
print("\n\n4️⃣ DECADE-WISE CONTENT PERFORMANCE")
print("-" * 60)
query4 = """
SELECT 
    Decade,
    COUNT(*) as Movies_Released,
    ROUND(AVG(IMDb), 2) as Avg_IMDb,
    ROUND(AVG("Rotten Tomatoes"), 1) as Avg_RT,
    ROUND(AVG(Runtime), 0) as Avg_Runtime
FROM movies
WHERE Decade >= 1950
GROUP BY Decade
ORDER BY Decade DESC;
"""
result4 = pd.read_sql_query(query4, conn)
print(result4.to_string(index=False))

# Query 5: Multi-Platform Content
print("\n\n5️⃣ MULTI-PLATFORM AVAILABILITY ANALYSIS")
print("-" * 60)
query5 = """
SELECT 
    Platform_Count as Num_Platforms,
    COUNT(*) as Movies,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM movies), 2) as Percentage,
    ROUND(AVG(Average_Rating), 2) as Avg_Rating
FROM movies
GROUP BY Platform_Count
ORDER BY Platform_Count;
"""
result5 = pd.read_sql_query(query5, conn)
print(result5.to_string(index=False))

# Query 6: Runtime Analysis
print("\n\n6️⃣ RUNTIME CATEGORY ANALYSIS")
print("-" * 60)
query6 = """
SELECT 
    Runtime_Category,
    COUNT(*) as Movie_Count,
    ROUND(AVG(Average_Rating), 2) as Avg_Rating,
    MIN(Runtime) as Min_Runtime,
    MAX(Runtime) as Max_Runtime
FROM movies
GROUP BY Runtime_Category
ORDER BY 
    CASE Runtime_Category
        WHEN 'Short' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Long' THEN 3
    END;
"""
result6 = pd.read_sql_query(query6, conn)
print(result6.to_string(index=False))

# Query 7: Recent High-Quality Content (2015-2020)
print("\n\n7️⃣ RECENT HIGH-QUALITY CONTENT (2015-2020)")
print("-" * 60)
query7 = """
SELECT 
    Title,
    Year,
    CASE 
        WHEN Netflix = 1 THEN 'Netflix, ' ELSE '' 
    END ||
    CASE 
        WHEN Hulu = 1 THEN 'Hulu, ' ELSE '' 
    END ||
    CASE 
        WHEN "Prime Video" = 1 THEN 'Prime Video, ' ELSE '' 
    END ||
    CASE 
        WHEN "Disney+" = 1 THEN 'Disney+' ELSE '' 
    END as Available_On,
    Average_Rating,
    Genres
FROM movies
WHERE Year >= 2015 
  AND Average_Rating >= 85
ORDER BY Average_Rating DESC
LIMIT 10;
"""
result7 = pd.read_sql_query(query7, conn)
print(result7.to_string(index=False))

# Query 8: Platform Exclusive Content Quality
print("\n\n8️⃣ PLATFORM EXCLUSIVE CONTENT (High Quality)")
print("-" * 60)
query8 = """
SELECT 
    CASE 
        WHEN Netflix = 1 THEN 'Netflix'
        WHEN Hulu = 1 THEN 'Hulu'
        WHEN "Prime Video" = 1 THEN 'Prime Video'
        WHEN "Disney+" = 1 THEN 'Disney+'
    END as Exclusive_Platform,
    COUNT(*) as Exclusive_Movies,
    ROUND(AVG(Average_Rating), 2) as Avg_Rating,
    COUNT(CASE WHEN Rating_Category = 'Excellent' THEN 1 END) as Excellent_Count
FROM movies
WHERE Platform_Count = 1
GROUP BY Exclusive_Platform
ORDER BY Exclusive_Movies DESC;
"""
result8 = pd.read_sql_query(query8, conn)
print(result8.to_string(index=False))

# Save all results to CSV for Tableau
print("\n\n💾 Saving query results for Tableau...")
result1.to_csv('/home/claude/sql_results/platform_overview.csv', index=False)
result3.to_csv('/home/claude/sql_results/content_strategy.csv', index=False)
result4.to_csv('/home/claude/sql_results/decade_performance.csv', index=False)
result5.to_csv('/home/claude/sql_results/multiplatform_analysis.csv', index=False)
result8.to_csv('/home/claude/sql_results/exclusive_content.csv', index=False)
print("   ✓ All query results saved to 'sql_results' folder")

# Close connection
conn.close()

print("\n" + "="*60)
print("✅ SQL ANALYSIS COMPLETE!")
print("="*60)
print("\nNext step: Create Tableau Dashboard")
print("\nSQL Files Created:")
print("   • streaming_analytics.db (SQLite database)")
print("   • sql_results/ (Query results for Tableau)")
