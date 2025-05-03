import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV from your local GitHub project folder
df = pd.read_csv(r'C:\Users\Gerar\Desktop\GitHub Repositories\crime_analysis_manhattan\SQL\BigQuery\most_common_offenses.csv')

# Preview the data
print(df.head())

# Optional: Rename columns if needed (adjust based on your actual column names)
# Example: df.columns = ['offense', 'count']

# Plot the most common offenses
plt.figure(figsize=(10, 6))
sns.barplot(x='count', y='offense', data=df.sort_values(by='count', ascending=False), palette='Blues_d')
plt.title('Most Common Offenses in the 9th Precinct (2021–2024)')
plt.xlabel('Number of Incidents')
plt.ylabel('Offense Type')
plt.tight_layout()

# Show the plot
plt.show()
