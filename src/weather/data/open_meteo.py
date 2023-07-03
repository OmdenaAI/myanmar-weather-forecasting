import requests
import pathlib
import pathlib
import pandas as pd


def main():
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": "21.00",
        "longitude": "96.00",
        "start_date": "2010-01-01",
        "end_date": "2023-06-17",
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,sunrise,sunset,shortwave_radiation_sum,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,et0_fao_evapotranspiration",
        "timezone": "GMT",
        "min": "2010-01-01",
        "max": "2023-06-17",
    }

    print("Querying weather API...")
    res = requests.get(url, params=params)

    if res.status_code != 200:
        res.raise_for_status()
        raise RuntimeError(f"Request to {url} returned status code {res.status_code}")

    data = res.json()

    # Convert data to tabular format and add some metadata
    print("Preprocessing...")
    df = pd.DataFrame(data["daily"])
    df["latitude"] = data["latitude"]
    df["longitude"] = data["longitude"]
    df["elevation"] = data["elevation"]
    df["country"] = "Myanmar"
    df["city"] = "Tha Phay Wa"

    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "weather"
    )
    file_name = "open_meteo.csv"

    df.to_csv(data_path / file_name, index=False)


if __name__ == "__main__":
    main()
