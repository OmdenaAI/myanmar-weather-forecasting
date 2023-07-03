# Data
This folder contains scripts to download data. Simply run them with `python path/to/file_name.py` to download the data to the [`data/weather`](/data/weather/) directory. Refer to June 24th's meeting recording for an example on how to run scripts.

## `open_meteo.py`
This script queries [open-meteo's Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) for **daily** weather data between January 1st, 2010 and June 17th, 2023. It then processes the response and downloads the result as a CSV file called `open_meteo.csv` in [`/data/weather`](/data/weather/).

The `open_meteo.csv` file contains information like min, max, mean temperature, precipitation, snowfall, wind speeds, coordinates of origin (latitude and longitude), country name, city name, etc. Some units used:
* Precipitation in millimiters
* Temperatures in Degrees Celsius
* Wind speeds in Kilometers/hour

## `berkley_cru.py`
This script uses data from two sources: [Berkley Earth](https://berkeley-earth-temperature-hr.s3.amazonaws.com/Gridded/Asia_TAVG_Gridded_1.nc) and [CRU (Climatic Research Unit)](https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/tmp/cru_ts4.07.1901.2022.tmp.dat.nc.gz). The data is downloaded and processed to contain information only about the country of Myanmar. It outputs two files **on NetCDF format**:

* `preprocessed_berk_myanmar.dat`: Contains information from Berkley Earth about Myanmar with records between January/1850 and January/2023, on a monthly frequency
* `preprocessed_cru_myanmar.dat`: Contains information from CRU about Myanmar with records between January/1910 and December/2022, on a monthly frequency

NetCDF is a very popular format in the cientific community, and one useful library to deal with data in this format is [xarray](https://docs.xarray.dev/en/stable/)
