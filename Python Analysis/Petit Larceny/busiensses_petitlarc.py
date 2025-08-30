import pandas as pd
from pandasql import sqldf
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
import os

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Load dataset
df = pd.read_csv(
    "C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan-1\\Data\\CLeaned Data\\PETIT LARCENY_9th_precinct_2024_2025.csv"
)

# SQL helper
pysqldf = lambda q: sqldf(q, globals())

# SQL query: Top 5 petit larceny locations
query = """
SELECT
    LOC_OF_OCCUR_DESC,
    Latitude,
    Longitude,
    COUNT(*) AS incident_count
FROM df
WHERE OFNS_DESC = 'PETIT LARCENY'
  AND Latitude IS NOT NULL
  AND Longitude IS NOT NULL
GROUP BY LOC_OF_OCCUR_DESC, Latitude, Longitude
ORDER BY incident_count DESC
LIMIT 5;
"""

top5_locations = pysqldf(query)

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(top5_locations['Longitude'], top5_locations['Latitude'])]
gdf = gpd.GeoDataFrame(top5_locations, geometry=geometry, crs="EPSG:4326")  # WGS84

# Reproject to Web Mercator for contextily
gdf = gdf.to_crs(epsg=3857)

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, markersize=gdf['incident_count']*50, color='red', alpha=0.6, edgecolor='k')

# Add basemap
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)

# Add labels for locations
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['LOC_OF_OCCUR_DESC']):
    ax.text(x, y, label, fontsize=8, ha='right', va='bottom', color='black')

ax.set_title("Top 5 Petit Larceny Locations – 9th Precinct (2024-2025)")
ax.set_axis_off()

# Save PNG
plt.tight_layout()
plt.savefig("output/top5_petit_larceny_nyc_map.png", dpi=300)
plt.show()
