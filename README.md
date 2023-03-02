[![Update daily data](https://github.com/jloayza10/Bolivia-Covid-19-app/actions/workflows/update_looker.yml/badge.svg)](https://github.com/jloayza10/Bolivia-Covid-19-app/actions/workflows/main.yml)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://covid19-bolivia.streamlit.app/)

# Covid-19 Bolivia App

This [Streamlit App](https://covid19-bolivia.streamlit.app/) 
presents Bolivia's Covid-19 data through several visualizations and formats.


## Details

The app allows to visualize information in different ways concerning positive cases, deaths and recovered cases.
Possible visualizations are:
- Tables
- Time-series plots
- Maps with information by department
Depending on the visualization chosen, daily, weekly, bi-weekly and monthly averages are possible. Also, some animations by date are presented.
The data is provided by the [Bolivian government](https://lookerstudio.google.com/u/0/reporting/92796894-acf3-4ab7-9395-20655de351f7/page/p_3ga366rsuc) and is scraped daily. The scraping method and code is inspired by [M. Foronda](https://github.com/sociedatos/covid19-bo-casos_por_departamento). This data is in no case the real data and in fact is surely undercounted.

All work was done in Python.
## Lessons Learned

While building this project, I was able to perform several tasks related to data visualization and coding in general.
- Data reading from several urls with pandas
- Data update with Github Actions and badge creation
- Data manipulation with melt, join, averages, missing data...
- Datatime and string manipulation
- Function creation and management
- Plotly syntax: 
    - basic plot syntax: scatter, bar
    - Layout updates
    - hover syntax, choropleth and choropleth_mapbox
- GeoJSON manipulation
- Streamlit documentation (different buttons, columns, plot size depending on number of plots selected...)
- Theme personalization (config.toml)
- Some CSS for footer personalization



## Further improvements
The presented app is functional and presents interesting daily data, but can always be improved:
- Error handling (for missing data, or when no department is chosen)
- Choropleth map with department name strings on
- Date on animation with spanish month name instead of number
- Code refactoring:
    - dataframe creation with a function when updating the scraped
    - In streamlit app, create more functions
- Vaccinaton and hospitalization data
- R<sub>0</sub> calculation
