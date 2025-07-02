import pandas as pd
from pandasql import sqldf
import os 

os.makedirs("output", exist_ok=True)


pysqldf = lambda q: sqldf(q, globals())

assault3df = pd.read_csv('C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\ASSAULT 3 & RELATED OFFENSES_9th_precinct_2024_2025.csv')

print(assault3df.head())

query1 = """
SELECT
    ADDR_PCT_CD,
    OFNS_DESC,
    CRM_ATPT_CPTD_CD,
    VIC_RACE,
    VIC_SEX AS vic_sex,
    COUNT(VIC_RACE)
FROM
    assault3df
WHERE 
    VIC_SEX = 'M' or VIC_SEX = 'F'
GROUP BY
    VIC_RACE, vic_sex
ORDER BY
    COUNT(VIC_RACE) DESC
"""

result1 = pysqldf(query1)
print(result1)

import seaborn as sns
import matplotlib.pyplot as plt

# Optional: rename columns for clarity
result1.columns = ['Precinct', 'Offense', 'Completion Status', 'Race', 'Sex', 'Count']

# Set up the figure size and style
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Create grouped bar chart
sns.barplot(data=result1, x='Race', y='Count', hue='Sex', palette='pastel')

# Title and labels
plt.title("Assault 3 Victim Count by Race and Sex (9th Precinct, 2024)", fontsize=14)
plt.xlabel("Victim Race")
plt.ylabel("Number of Victims")
plt.xticks(rotation=45)

# Save image for GitHub
plt.tight_layout()
plt.savefig("output/assault3_victim_race_sex.png")
plt.show()
