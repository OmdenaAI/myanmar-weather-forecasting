# Data
This folder contains scripts to download data. Simply run them with `python path/to/file_name.py` to download the data to the [`data/weather`](/data/weather/) directory. Refer to June 24th's meeting recording for an example on how to run scripts.

## `open_meteo.py`
This script queries [open-meteo's Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) for **daily** weather data between January 1st, 2010 and June 17th, 2023. It then processes the response and downloads the result as a CSV file called `open_meteo.csv` in [`/data/weather`](/data/weather/).

The `open_meteo.csv` file contains information like min, max, mean temperature, precipitation, snowfall, wind speeds, coordinates of origin (latitude and longitude), country name, city name, etc. Some units used:
* Precipitation in millimiters
* Temperatures in Degrees Celsius
* Wind speeds in Kilometers/hour