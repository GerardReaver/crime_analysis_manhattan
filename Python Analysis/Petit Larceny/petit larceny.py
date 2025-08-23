# This imports all the packages i will need for this analysis of petit larceny
import pandas as pd
from pandasql import sqldf
import os
import folium
import matplotlib.pyplot as plt

# enabling SQL queries with this function
pysqldf = lambda q: sqldf(q, globals()) 

petitlarcenydf = pd.read_csv(
    "C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\PETIT LARCENY_9th_precinct_2024_2025.csv"
)

# preview the data
print(petitlarcenydf.head())

# Group by victim sex
victim_counts = petitlarcenydf['VIC_SEX'].value_counts()

# Mapping codes to descriptive labels
victim_labels = {
    'F': 'Female',
    'M': 'Male',
    'U': 'Unknown',
    'D': 'Business'
}

# Replace codes with full names
petitlarcenydf['VIC_SEX_LABEL'] = petitlarcenydf['VIC_SEX'].map(victim_labels)

# Group and count
victim_counts = petitlarcenydf['VIC_SEX_LABEL'].value_counts()

# Plot pie chart
plt.figure(figsize=(6,6))
plt.pie(
    victim_counts,
    labels=victim_counts.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Petit Larceny Victims by Sex (2024-2025)')
plt.show()

plt.savefig("visuals/petit_larceny_victim_sex.png")

