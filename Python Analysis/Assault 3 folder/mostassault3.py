import folium
import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

# Load your filtered data from earlier
assault3df = pd.read_csv('C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\ASSAULT 3 & RELATED OFFENSES_9th_precinct_2024_2025.csv')

# Make sure date is in datetime format
assault3df['CMPLNT_FR_DT'] = pd.to_datetime(assault3df['CMPLNT_FR_DT'], errors='coerce')

# Filter for busiest day via SQL
query1 = """
SELECT 
    CMPLNT_FR_DT,
    COUNT(*) AS report_count
FROM
    assault3df
WHERE
    CMPLNT_FR_DT != '(null)'
GROUP BY
    CMPLNT_FR_DT
ORDER BY
    report_count DESC
LIMIT 10
"""
top_day_df = pysqldf(query1)
top_date = top_day_df.iloc[0]['CMPLNT_FR_DT']

# Get only incidents from that top day
query2 = f"""
SELECT
    CMPLNT_FR_DT,
    CMPLNT_FR_TM,
    Lat_Lon
FROM
    assault3df
WHERE
    CMPLNT_FR_DT = '{top_date}'
    AND Lat_Lon != '(null)'
"""
result1 = pysqldf(query2)

# Split Lat_Lon
result1[['Latitude', 'Longitude']] = result1['Lat_Lon'] \
    .str.strip('()') \
    .str.split(',', expand=True)

result1['Latitude'] = result1['Latitude'].astype(float)
result1['Longitude'] = result1['Longitude'].astype(float)

# Drop invalid rows
map_df = result1.dropna(subset=['Latitude', 'Longitude'])

# Center map on Manhattan
m = folium.Map(location=[40.73, -73.99], zoom_start=13, tiles="CartoDB positron")

# Add each assault as a red dot
for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f"Time: {row['CMPLNT_FR_TM']}"
    ).add_to(m)

# Save map
m.save("output/assault3_top_day_map.html")
