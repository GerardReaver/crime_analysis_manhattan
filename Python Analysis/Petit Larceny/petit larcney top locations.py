import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt

# 1. Load your dataset
top_petit_larceny_locsdf = pd.read_csv(
    "C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan-1\\Data\\CLeaned Data\\PETIT LARCENY_9th_precinct_2024_2025.csv"
)

# 2. SQL query: Top 5 premises for petit larceny
query = """
SELECT 
    PREM_TYP_DESC,
    COUNT(*) as incident_count
FROM
    top_petit_larceny_locsdf
WHERE
    OFNS_DESC = 'PETIT LARCENY'
GROUP BY
    PREM_TYP_DESC
ORDER BY
    incident_count DESC
LIMIT 
    5;
"""

top5_businesses = ps.sqldf(query, locals())

# 3. Bar Chart with matplotlib
plt.figure(figsize=(8,6))
plt.bar(top5_businesses['PREM_TYP_DESC'], top5_businesses['incident_count'], color='skyblue')

# 4. Titles + labels
plt.title("Top 5 Locations for Petit Larceny (NYPD 9th Precinct, 2024–2025)")
plt.xlabel("Business Type")
plt.ylabel("Incident Count")
plt.xticks(rotation=30, ha='right')  # tilt labels for readability

# 5. Show chart
plt.tight_layout()
plt.show()
