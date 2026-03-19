"""
STEP 3: Exploratory Data Analysis (EDA)
This script analyzes the data and creates visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Load cleaned data
print("Loading cleaned dataset...")
df = pd.read_csv('/home/claude/streaming_data_clean.csv')

print("\n" + "="*60)
print("EXPLORATORY DATA ANALYSIS")
print("="*60)

# Create visualizations directory
import os
os.makedirs('/home/claude/visualizations', exist_ok=True)

# 1. PLATFORM ANALYSIS
print("\n1️⃣ Platform Content Analysis...")
platform_counts = {
    'Netflix': df['Netflix'].sum(),
    'Hulu': df['Hulu'].sum(),
    'Prime Video': df['Prime Video'].sum(),
    'Disney+': df['Disney+'].sum()
}

plt.figure(figsize=(10, 6))
bars = plt.bar(platform_counts.keys(), platform_counts.values(), 
               color=['#E50914', '#1CE783', '#00A8E1', '#113CCF'])
plt.title('Number of Movies per Streaming Platform', fontsize=16, fontweight='bold')
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Number of Movies', fontsize=12)
plt.xticks(rotation=0)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/claude/visualizations/01_platform_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 01_platform_distribution.png")

# 2. RATING DISTRIBUTION
print("\n2️⃣ Rating Distribution Analysis...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# IMDb distribution
axes[0].hist(df['IMDb'], bins=30, color='#FF6B6B', edgecolor='black', alpha=0.7)
axes[0].axvline(df['IMDb'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["IMDb"].mean():.2f}')
axes[0].set_title('IMDb Rating Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('IMDb Rating', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].legend()
axes[0].grid(alpha=0.3)

# Rotten Tomatoes distribution
axes[1].hist(df['Rotten Tomatoes'], bins=30, color='#4ECDC4', edgecolor='black', alpha=0.7)
axes[1].axvline(df['Rotten Tomatoes'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Rotten Tomatoes"].mean():.2f}')
axes[1].set_title('Rotten Tomatoes Score Distribution', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Rotten Tomatoes Score', fontsize=11)
axes[1].set_ylabel('Frequency', fontsize=11)
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/visualizations/02_rating_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 02_rating_distributions.png")

# 3. CONTENT TRENDS OVER TIME
print("\n3️⃣ Content Release Trends...")
yearly_counts = df.groupby('Year').size()

plt.figure(figsize=(14, 6))
plt.plot(yearly_counts.index, yearly_counts.values, linewidth=2.5, color='#FF6B6B', marker='o', markersize=3)
plt.fill_between(yearly_counts.index, yearly_counts.values, alpha=0.3, color='#FF6B6B')
plt.title('Movies Released by Year (1902-2020)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Movies Released', fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/home/claude/visualizations/03_yearly_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 03_yearly_trends.png")

# 4. DECADE ANALYSIS
print("\n4️⃣ Decade-wise Analysis...")
decade_avg = df.groupby('Decade').agg({
    'Average_Rating': 'mean',
    'Title': 'count'
}).reset_index()
decade_avg.columns = ['Decade', 'Avg_Rating', 'Movie_Count']

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

bar_plot = ax1.bar(decade_avg['Decade'], decade_avg['Movie_Count'], 
                    color='#95E1D3', alpha=0.7, label='Movie Count')
line_plot = ax2.plot(decade_avg['Decade'], decade_avg['Avg_Rating'], 
                     color='#F38181', marker='o', linewidth=3, markersize=8, label='Avg Rating')

ax1.set_xlabel('Decade', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Movies', fontsize=12, fontweight='bold', color='#95E1D3')
ax2.set_ylabel('Average Rating', fontsize=12, fontweight='bold', color='#F38181')
ax1.set_title('Movies Released and Average Rating by Decade', fontsize=16, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#95E1D3')
ax2.tick_params(axis='y', labelcolor='#F38181')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig('/home/claude/visualizations/04_decade_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 04_decade_analysis.png")

# 5. RUNTIME ANALYSIS
print("\n5️⃣ Runtime Analysis...")
runtime_dist = df['Runtime_Category'].value_counts()

colors = ['#FFB6B9', '#FEC8D8', '#FFDFD3']
plt.figure(figsize=(10, 6))
plt.pie(runtime_dist.values, labels=runtime_dist.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
plt.title('Distribution of Movie Runtimes', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/claude/visualizations/05_runtime_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 05_runtime_distribution.png")

# 6. PLATFORM OVERLAP
print("\n6️⃣ Multi-Platform Availability...")
platform_count_dist = df['Platform_Count'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
bars = plt.bar(platform_count_dist.index, platform_count_dist.values, 
               color=['#667BC6', '#DA7297', '#FADA7A', '#82CD47'])
plt.title('Movies by Number of Platforms', fontsize=16, fontweight='bold')
plt.xlabel('Number of Platforms', fontsize=12)
plt.ylabel('Number of Movies', fontsize=12)
plt.xticks([1, 2, 3, 4])
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/claude/visualizations/06_platform_overlap.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 06_platform_overlap.png")

# 7. TOP GENRES ANALYSIS
print("\n7️⃣ Genre Analysis...")
# Extract first genre from each movie
df['Primary_Genre'] = df['Genres'].str.split(',').str[0]
top_genres = df['Primary_Genre'].value_counts().head(10)

plt.figure(figsize=(12, 6))
bars = plt.barh(top_genres.index, top_genres.values, color='#7BC9FF')
plt.title('Top 10 Most Common Genres', fontsize=16, fontweight='bold')
plt.xlabel('Number of Movies', fontsize=12)
plt.ylabel('Genre', fontsize=12)
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
             f' {int(width):,}',
             ha='left', va='center', fontsize=11, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/home/claude/visualizations/07_top_genres.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 07_top_genres.png")

# 8. AVERAGE RATING BY PLATFORM
print("\n8️⃣ Platform Quality Comparison...")
platform_ratings = []
for platform in ['Netflix', 'Hulu', 'Prime Video', 'Disney+']:
    avg_rating = df[df[platform] == 1]['Average_Rating'].mean()
    platform_ratings.append({'Platform': platform, 'Avg_Rating': avg_rating})

platform_df = pd.DataFrame(platform_ratings)

plt.figure(figsize=(10, 6))
bars = plt.bar(platform_df['Platform'], platform_df['Avg_Rating'], 
               color=['#E50914', '#1CE783', '#00A8E1', '#113CCF'])
plt.title('Average Content Rating by Platform', fontsize=16, fontweight='bold')
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)
plt.ylim(0, 100)
plt.axhline(y=df['Average_Rating'].mean(), color='red', linestyle='--', 
            linewidth=2, label=f'Overall Avg: {df["Average_Rating"].mean():.1f}')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig('/home/claude/visualizations/08_platform_quality.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 08_platform_quality.png")

# 9. CORRELATION HEATMAP
print("\n9️⃣ Correlation Analysis...")
correlation_cols = ['IMDb', 'Rotten Tomatoes', 'Runtime', 'Year', 'Average_Rating', 'Platform_Count']
correlation_matrix = df[correlation_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            fmt='.2f', annot_kws={'fontsize': 10, 'fontweight': 'bold'})
plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/home/claude/visualizations/09_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 09_correlation_heatmap.png")

# Print key insights
print("\n" + "="*60)
print("KEY INSIGHTS")
print("="*60)
print(f"\n📊 Content Statistics:")
print(f"   • Total Movies: {len(df):,}")
print(f"   • Average IMDb Rating: {df['IMDb'].mean():.2f}")
print(f"   • Average Rotten Tomatoes: {df['Rotten Tomatoes'].mean():.1f}%")
print(f"   • Average Runtime: {df['Runtime'].mean():.0f} minutes")

print(f"\n🎬 Platform Leader:")
print(f"   • Most Content: Prime Video ({df['Prime Video'].sum():,} movies)")
print(f"   • Highest Avg Rating: {platform_df.loc[platform_df['Avg_Rating'].idxmax(), 'Platform']}")

print(f"\n📅 Timeline:")
print(f"   • Oldest Movie: {df['Year'].min()}")
print(f"   • Most Recent: {df['Year'].max()}")
print(f"   • Peak Release Year: {df.groupby('Year').size().idxmax()}")

print(f"\n🎭 Most Common Genre: {top_genres.index[0]}")

exclusive_content = df[df['Platform_Count'] == 1]
print(f"\n🔒 Exclusive Content: {len(exclusive_content):,} movies ({len(exclusive_content)/len(df)*100:.1f}%)")

print("\n✅ EDA Complete! All visualizations saved in 'visualizations' folder")
print("Next step: SQL Analysis")
