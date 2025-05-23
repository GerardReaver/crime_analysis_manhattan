import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

assault3df = pd.read_csv('C:\\Users\\Gerar\\Desktop\\GitHub Repositories\\crime_analysis_manhattan\\Data\\CLeaned Data\\ASSAULT 3 & RELATED OFFENSES_9th_precinct_2024_2025.csv')

print(assault3df.head())

query1 = """
SELECT
    ADDR_PCT_CD,
    SUSP_AGE_GROUP AS perp_age,
    SUSP_RACE AS perp_race,
    SUSP_SEX AS perp_sex,
    OFNS_DESC,
    CRM_ATPT_CPTD_CD,
    VIC_RACE,
    COUNT(VIC_RACE),
    VIC_SEX AS vic_sex
FROM
    assault3df
WHERE
    perp_race = 'BLACK'
GROUP BY
    VIC_RACE, vic_sex
ORDER BY
    COUNT(VIC_RACE) DESC
"""

result1 = pysqldf(query1)
print(result1)