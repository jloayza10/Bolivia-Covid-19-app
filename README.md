[![Update daily data](https://github.com/jloayza10/Bolivia-Covid-19-app/actions/workflows/update_looker.yml/badge.svg)](https://github.com/jloayza10/Bolivia-Covid-19-app/actions/workflows/main.yml)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://covid19-bolivia.streamlit.app/)

# Covid-19 Bolivia App

The [Covid-19 Bolivia App](https://covid19-bolivia.streamlit.app/) 
is a Streamlit-based web application that offers users several visualization tools for presenting Covid-19 data from Bolivia in a variety of formats.


## Details

The app provides three types of visualizations:
- tables
- time-series plots
- maps by department

Daily, weekly, bi-weekly and monthly averages are available depending on the type of visualization. Date animations are also available depending on the visualization chosen.
The data is provided by the [Bolivian government](https://lookerstudio.google.com/u/0/reporting/92796894-acf3-4ab7-9395-20655de351f7/page/p_3ga366rsuc). The scraping method and code is inspired by [M. Foronda](https://github.com/sociedatos/covid19-bo-casos_por_departamento). This data is scraped daily, but it is a clear undercount.

All work was done in Python.
## Lessons Learned

The app provides insights and some lessons learned related to data visualization and coding, including:
- Data collection via Pandas
- Data update with Github Actions and badge creation
- Data manipulation techniques such as melt, join, averages, and managing missing data.
- Datatime and string manipulation skills
- Function creation and management
- Plotly syntax for plots including basic plot syntax, Layout updates, and hover syntax, choropleth and choropleth_mapbox.
- Use the gettext system for translating the displayed text from Spanish to English. Use of pygettext and msgfmt commands, .po and .mo file creation and solve issues with translatable strings which are also variables such as column names for the dataframes.
- GeoJSON manipulation
- Streamlit documentation knowledge (different buttons, columns, plot size selection, among others).
- Theme personalization using config.toml
- Some CSS knowledge for footer personalization



## Further improvements
The app is functional and provides relevant daily data, but there is still room for improvement:
- Error handling for missing data or when no department is chosen (Done)
- Choropleth map with department name strings on
- Code refactoring:
    - Creation of more functions
- Inclusion of vaccination and hospitalization data
- R<sub>0</sub> calculation
