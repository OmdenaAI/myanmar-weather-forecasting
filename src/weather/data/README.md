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

## `berkley_cru.py`
This script uses data from two sources: [Berkley Earth](https://berkeley-earth-temperature-hr.s3.amazonaws.com/Gridded/Asia_TAVG_Gridded_1.nc) and [CRU (Climatic Research Unit)](https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/tmp/cru_ts4.07.1901.2022.tmp.dat.nc.gz). The data is downloaded and processed to contain information only about the country of Myanmar. It outputs two files **on NetCDF format**:

* `preprocessed_berk_myanmar.dat`: Contains information from Berkley Earth about Myanmar with records between January/1850 and January/2023, on a monthly frequency
* `preprocessed_cru_myanmar.dat`: Contains information from CRU about Myanmar with records between January/1910 and December/2022, on a monthly frequency

NetCDF is a very popular format in the cientific community, and one useful library to deal with data in this format records is [xarray](https://docs.xarray.dev/en/stable/)