import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Set Seaborn theme
sns.set_theme(style="whitegrid")

# List of Excel files (adjust paths if needed)
years = ['2015_2016', '2016_2017', '2017_2018', '2018_2019', '2019_2020',
         '2020_2021', '2021_2022', '2022_2023', '2023_2024']

files = [f'CIS_byProvider_Tier2and3Support_{year}.xlsx' for year in years]

# List to store dataframes
dfs = []

# Read and process each file
for year, file in zip(years, files):
    df = pd.read_excel(file, header=1)
    df.columns = df.columns.str.strip().str.replace('\n', ' ', regex=True)
    df['Year'] = year
    df['Total Supports'] = df['# of Tier II Supports'] + df['# of Tier III Supports']
    df['Total Hours'] = df['# of Tier II Hours'] + df['# of Tier III Hours']
    dfs.append(df)

# Combine all years into one DataFrame
full_df = pd.concat(dfs)

# ======================= VISUALIZATIONS ===========================

# 1. Pie Chart: Total Supports Distribution by Student Support Category (All Years Combined)
category_totals = full_df.groupby('Student Support Category')['Total Supports'].sum()
plt.figure(figsize=(8, 8))
category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Supports Distribution by Student Support Category (All Years)')
plt.ylabel('')
plt.tight_layout()
plt.savefig("charts/supports_by_category_pie.png")
plt.show()

# 2. Stacked Bar: Tier II vs Tier III Supports by Category
tier_totals = full_df.groupby('Student Support Category')[['# of Tier II Supports', '# of Tier III Supports']].sum()
tier_totals.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Tier II vs Tier III Supports by Category (All Years)')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Number of Supports')
plt.tight_layout()
plt.savefig("charts/tier2_tier3_stacked_bar.png")
plt.show()

# 3. Bar: Total Support Hours by School
plt.figure(figsize=(12, 6))
sns.barplot(data=full_df, x='School Where Support Was Provided', y='Total Hours', estimator=sum, ci=None)
plt.title('Total Support Hours by School (All Years)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("charts/support_hours_by_school_bar.png")
plt.show()

# 4. Line Plot: Total Supports Over the Years
yearly_totals = full_df.groupby('Year')['Total Supports'].sum().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=yearly_totals, x='Year', y='Total Supports', marker='o')
plt.title('Total Supports Over the Years')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/total_supports_over_years_line.png")
plt.show()

# 5. Grouped Bar: Total Supports by Provider Type and Year
provider_year_totals = full_df.groupby(['Year', 'Provider Type'])['Total Supports'].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(data=provider_year_totals, x='Year', y='Total Supports', hue='Provider Type')
plt.title('Total Supports by Provider Type Across Years')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/supports_by_provider_and_year_bar.png")
plt.show()

# 6. Donut Chart: Total Supports by Activity (All Years)
activity_totals = full_df.groupby('Activity')['Total Supports'].sum()
plt.figure(figsize=(8, 8))
plt.pie(activity_totals, labels=activity_totals.index, autopct='%1.1f%%', startangle=90)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Supports by Activity (All Years)')
plt.tight_layout()
plt.savefig("charts/supports_by_activity_donut.png")
plt.show()

# 7. Bar: Total Supports by Student Support Category and Year
category_year_totals = full_df.groupby(['Year', 'Student Support Category'])['Total Supports'].sum().reset_index()
plt.figure(figsize=(14, 6))
sns.barplot(data=category_year_totals, x='Year', y='Total Supports', hue='Student Support Category')
plt.title('Supports by Student Support Category Across Years')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/supports_by_category_and_year_bar.png")
plt.show()

print("✅ All charts generated and saved in the 'charts' folder!")
