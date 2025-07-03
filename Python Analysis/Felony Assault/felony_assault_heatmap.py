import pandas as pd
from pandasql import sqldf
import folium
import os

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Enable SQL on DataFrame
pysqldf = lambda q: sqldf(q, globals())

# Load your FELONY ASSAULT CSV file
felony_df = pd.read_csv(
    "C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\FELONY ASSAULT_9th_precinct_2024_2025.csv"
)

# SQL query: Top 50 most frequent Lat_Lon locations
query1 = """
SELECT
    Lat_Lon,
    COUNT(*) AS assault_count
FROM
    felony_df
WHERE
    Lat_Lon != '(null)'
GROUP BY
    Lat_Lon
ORDER BY
    assault_count DESC
LIMIT 50
"""

# Run the SQL query
result1 = pysqldf(query1)

# Clean and split Lat_Lon column
result1[['Latitude', 'Longitude']] = result1['Lat_Lon'] \
    .str.strip('()') \
    .str.split(',', expand=True)

# Convert coordinates to float
result1['Latitude'] = result1['Latitude'].astype(float)
result1['Longitude'] = result1['Longitude'].astype(float)

# Drop invalid rows
result1 = result1.dropna(subset=['Latitude', 'Longitude'])

# Create an interactive Folium map centered on the 9th Precinct
felony_map = folium.Map(
    location=[40.726, -73.987],  # NYPD 9th Precinct area
    zoom_start=14,
    tiles="CartoDB positron"
)

# Plot top 50 felony assault locations
for _, row in result1.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=4 + (row['assault_count'] * 0.8),  # radius scaled by count
        color='darkred',
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        popup=f"Felony Assaults: {row['assault_count']}"
    ).add_to(felony_map)

# Save the map to HTML
felony_map.save("output/top_50_felony_assault_hotspots_map.html")
print("✅ Map saved to: output/top_50_felony_assault_hotspots_map.html")
