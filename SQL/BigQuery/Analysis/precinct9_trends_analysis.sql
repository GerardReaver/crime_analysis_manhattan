-- Query 1: Monthly Crime Trends
SELECT 
  year,
  month,
  COUNT(*) AS total_complaints
FROM `fleet-karma-342102.nypd_crime_data.precinct9_cleaned`
GROUP BY year, month
ORDER BY year, month;

-- Query 2: Most Common Offense Types
SELECT 
  OFNS_DESC,
  COUNT(*) AS complaint_count
FROM `fleet-karma-342102.nypd_crime_data.precinct9_cleaned`
GROUP BY OFNS_DESC
ORDER BY complaint_count DESC
LIMIT 15;

-- Query 3: Crime by Law Category
SELECT 
  LAW_CAT_CD,
  COUNT(*) AS complaint_count
FROM `fleet-karma-342102.nypd_crime_data.precinct9_cleaned`
GROUP BY LAW_CAT_CD
ORDER BY complaint_count DESC;
