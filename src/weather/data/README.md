# Data
This folder contains scripts to download data. Simply run them with `python file_name.py` to download the data to the [`data/weather`](/data/weather/) directory

## `open_meteo.py`
This script queries [open-meteo's Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) for **daily** weather data between January 1st, 2010 and June 17th, 2023. It then downloads the response as a JSON file called `open_meteo.json` in [`/data/weather`](/data/weather/).

It contains information like min, max, mean temperature, precipitation, snowfall, wind speeds, etc. The JSON file also has metadata, like the data origin (coordinates) and the units of measure for each feature. Some units used:
* Millimiters are used for precipitation
* Degrees Celsius are used for temperature
* Kilometers/hour are used for wind speeds.

The interesting part of the data is in the key `daily`. The `open_meteo.json` file is roughly organized in the following format:
```javascript
{
    // ...a bunch of keys with metadata like "latitude", "longitude", "units"
    "daily": {
        "feature1": [1, 2, 3],
        "feature2": ["val1", "val2", "val3"],
        ...
    }
}
```