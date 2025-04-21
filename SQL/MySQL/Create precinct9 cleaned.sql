CREATE OR REPLACE TABLE `fleet-karma-342102.nypd_crime_data.precinct9_cleaned` AS
SELECT 
  CMPLNT_NUM,
  CMPLNT_FR_DT AS complaint_date,
  OFNS_DESC,
  LAW_CAT_CD,
  KY_CD,
  PD_DESC,
  latitude,
  longitude,
  ADDR_PCT_CD,
  BORO_NM,
  EXTRACT(YEAR FROM CMPLNT_FR_DT) AS year,
  EXTRACT(MONTH FROM CMPLNT_FR_DT) AS month
FROM `fleet-karma-342102.nypd_crime_data.complaint_current`
WHERE 
  ADDR_PCT_CD = 9
  AND CMPLNT_FR_DT BETWEEN DATE '2022-01-01' AND DATE '2024-12-31'

UNION ALL

SELECT 
  CMPLNT_NUM,
  CMPLNT_FR_DT AS complaint_date,
  OFNS_DESC,
  LAW_CAT_CD,
  KY_CD,
  PD_DESC,
  latitude,
  longitude,
  ADDR_PCT_CD,
  BORO_NM,
  EXTRACT(YEAR FROM CMPLNT_FR_DT) AS year,
  EXTRACT(MONTH FROM CMPLNT_FR_DT) AS month
FROM `fleet-karma-342102.nypd_crime_data.complaint_historic`
WHERE 
  ADDR_PCT_CD = 9
  AND CMPLNT_FR_DT BETWEEN DATE '2022-01-01' AND DATE '2024-12-31';
