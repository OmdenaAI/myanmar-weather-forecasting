# Data
This folder contains scripts to download data. Simply run them with `python file_name.py` to download the data to the [`data`](/data/) directory

## `open_meteo.py`
This script queries [open-meteo's Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) for **daily** weather data between January 1st, 2010 and June 17th, 2023. It then downloads the response as a JSON file called `open_meteo.json` in [`/data/weather](/data/weather/).

It contains information like min, max, mean temperature, precipitation, snowfall, wind speeds, etc. The JSON file also has metadata, like the data origin (coordinates) and the units of measure for each feature. Some units used:
* Millimiters are used for precipitation
* Degrees Celsius are used for temperature
* Kilometers/hour are used for wind speeds.

The JSON key `daily` contais the data. It's organized in the following format:
```JSON
"daily": {
    "feature1": [f1_value1, f1_value2, ...],
    "feature2": [f2_value1, f2_value2, ...],
    .
    .
    .
}

```