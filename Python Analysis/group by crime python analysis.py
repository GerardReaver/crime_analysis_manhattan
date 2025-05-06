import pandas as pd

# Load the data (replace with your correct path)
data = pd.read_csv(r'C:\Users\Gerar\Downloads\NYPD_Complaint_Data_Historic_20250505.csv')

# Filter data for the 9th precinct using the correct column 'ADDR_PCT_CD'
data_9th_precinct = data[data['ADDR_PCT_CD'] == 9]

# Drop rows with missing latitude, longitude, or crime type (for heatmap visualization)
data_9th_precinct_clean = data_9th_precinct.dropna(subset=['Latitude', 'Longitude', 'OFNS_DESC'])

# Get the list of unique crime types from 'OFNS_DESC'
crime_types = data_9th_precinct_clean['OFNS_DESC'].unique()

# Save separate CSV files for each crime type
for crime in crime_types:
    crime_data = data_9th_precinct_clean[data_9th_precinct_clean['OFNS_DESC'] == crime]
    crime_data.to_csv(f'C:/Users/Gerar/Downloads/{crime}_9th_precinct_2024_2025.csv', index=False)

    print(f"Saved data for {crime} to CSV.")
