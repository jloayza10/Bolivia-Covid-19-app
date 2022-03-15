Step 1 - Data Parsing

In this step, the file data_read_processing.py reads, parses and transforms Covid-19 data from 
https://raw.githubusercontent.com/sociedatos/covid19-bo-casos_por_departamento/master/
and saves it in pickle format in the data folder. The 3 dataframes saved are:
- df_covid_Bolivia: contains daily and total positive cases, deaths and recovered for each bolivian
department and also calculates the total for the country.
- df_monthly_mean: contains monthly means
- df_weekly_mean: contains weekly means