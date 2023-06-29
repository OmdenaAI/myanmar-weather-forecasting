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

## `climate_research_unit.py`
The code is designed to download and extract climate data from the CRU (Climatic Research Unit) dataset. It focuses specifically on the temperature data for the period from 1901 to 2022. This is a spatio-temporal dataset

Here's a breakdown of what the code does:

* The URL variable is set to the location of the dataset file to be downloaded.
* It specifies the path where the downloaded and extracted data file will be saved.
* A GET request is sent to the URL using the requests module, retrieving the dataset file.
* The response status code is checked. If the code is 200 (indicating a successful request), the file is saved.
* The file is saved in the specified data_path directory with the name "cru_ts4.07.1901.2022.tmp.dat.nc.gz". The response content is written to the file using the "wb" (write binary) mode.
* If the request is not successful (status code other than 200), an error message is printed indicating the failure.

## `berkely_earth.py`
The code provided retrieves a specific URL, scrapes the HTML content of the page, and searches for a link with the specified href attribute. It then attempts to download the file associated with that link and save it to a specified directory.

Here's how the code works:

* The URL variable is set to the desired URL of the Berkeley Earth data page.
* It specifies the path where the downloaded and extracted data file will be saved.
* A GET request is sent to the URL using the requests module to retrieve the HTML content of the page.
* The HTML content is parsed using BeautifulSoup and stored in the soup variable.
* The code searches for a specific link with the href attribute matching the given value. If the link is found, the URL of the Asia data is extracted from the href attribute and stored in the asia_data_url variable. If the link is not found, an appropriate message is printed.
* Another GET request is sent to the Asia data URL to download the file.
* The code checks if the request was successful by verifying the response status code. If it is 200 (indicating a successful request), the file is saved.
* The file is saved in the specified data_path directory with the name extracted from the asia_data_url. The response content is written to the file using the "wb" (write binary) mode.
* If the request is not successful (status code other than 200), an error message is printed.
