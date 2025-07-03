import pandas as pd
from pandasql import sqldf
import folium
import os

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Enable SQL on DataFrame
pysqldf = lambda q: sqldf(q, globals())

# Load your cleaned CSV
assault3df = pd.read_csv(
    'C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\ASSAULT 3 & RELATED OFFENSES_9th_precinct_2024_2025.csv'
)

# SQL query: Top 50 locations with most assault reports
query1 = """
SELECT
    Lat_Lon,
    COUNT(*) AS assault_count
FROM
    assault3df
WHERE
    Lat_Lon != '(null)'
GROUP BY
    Lat_Lon
ORDER BY
    assault_count DESC
LIMIT 50
"""

# Run query
result1 = pysqldf(query1)

# Clean and split Lat_Lon into Latitude and Longitude
result1[['Latitude', 'Longitude']] = result1['Lat_Lon'] \
    .str.strip('()') \
    .str.split(',', expand=True)

# Convert to float
result1['Latitude'] = result1['Latitude'].astype(float)
result1['Longitude'] = result1['Longitude'].astype(float)

# Drop invalids if needed
result1 = result1.dropna(subset=['Latitude', 'Longitude'])

# Create folium map centered on 9th Precinct
hotspot_map = folium.Map(
    location=[40.726, -73.987],
    zoom_start=14,
    tiles="CartoDB positron"
)

# Plot each location with scaled circle marker
for _, row in result1.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=4 + (row['assault_count'] * 0.8),  # size based on count
        color='crimson',
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        popup=f"Assault Count: {row['assault_count']}"
    ).add_to(hotspot_map)

# Save map to HTML file
hotspot_map.save("output/top_50_assault_hotspots_map.html")
print("✅ Map saved to: output/top_50_assault_hotspots_map.html")
