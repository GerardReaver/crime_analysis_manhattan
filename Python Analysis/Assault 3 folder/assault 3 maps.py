import pandas as pd
from pandasql import sqldf
import os
import folium

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Enable SQL queries on DataFrame
pysqldf = lambda q: sqldf(q, globals())

# Load the cleaned CSV file
assault3df = pd.read_csv(
    'C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\ASSAULT 3 & RELATED OFFENSES_9th_precinct_2024_2025.csv'
)

# Preview
print(assault3df.head())

# Query data: Filter by day-shift time and remove "(null)"
query1 = """
SELECT
    ADDR_PCT_CD, 
    CMPLNT_FR_TM,
    CMPLNT_TO_TM,
    Lat_Lon
FROM
    assault3df
WHERE
    CMPLNT_FR_TM > '07:00:00' 
    AND CMPLNT_TO_TM < '15:40:00'
    AND CMPLNT_FR_TM != '(null)'
    AND CMPLNT_TO_TM != '(null)'
"""
result1 = pysqldf(query1)
print(result1.head())

# Clean Lat_Lon column
result1 = result1[result1['Lat_Lon'] != '(null)']
result1 = result1.dropna(subset=['Lat_Lon'])

# Split Lat_Lon into Latitude and Longitude
result1[['Latitude', 'Longitude']] = result1['Lat_Lon'] \
    .str.strip('()') \
    .str.split(',', expand=True)

# Convert strings to float
result1['Latitude'] = result1['Latitude'].astype(float)
result1['Longitude'] = result1['Longitude'].astype(float)

# Drop invalid rows
map_df = result1.dropna(subset=['Latitude', 'Longitude'])

# Create interactive map centered on NYPD 9th Precinct (Lower Manhattan)
manhattan_map = folium.Map(
    location=[40.726, -73.987],  # Approximate center of the 9th Precinct
    zoom_start=14,
    tiles="CartoDB positron"
)

# Add markers to the map
for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f"From: {row['CMPLNT_FR_TM']}<br>To: {row['CMPLNT_TO_TM']}"
    ).add_to(manhattan_map)

# Save map to HTML file
manhattan_map.save("output/assault3_day_shift_map_manhattan.html")
print("✅ Map saved as 'output/assault3_day_shift_map_manhattan.html'")
