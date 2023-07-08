import requests
import pathlib
import pandas as pd


def main():
    url = "https://archive-api.open-meteo.com/v1/archive"
    # fmt: off
    cities = [
        { "name": "Jakarta", "country": "Indonesia", "latitude": -6.175, "longitude": 106.8275 },
        { "name": "Surabaya", "country": "Indonesia", "latitude": -7.2458, "longitude": 112.7378 },
        { "name": "Medan", "country": "Indonesia", "latitude": 3.5894, "longitude": 98.6739 },
        { "name": "Malang", "country": "Indonesia", "latitude": -7.98, "longitude": 112.62 },
        { "name": "Bekasi", "country": "Indonesia", "latitude": -6.2349, "longitude": 106.9923 },
        { "name": "Depok", "country": "Indonesia", "latitude": -6.394, "longitude": 106.8225 },
        { "name": "Tangerang", "country": "Indonesia", "latitude": -6.1783, "longitude": 106.6319 },
        { "name": "Denpasar", "country": "Indonesia", "latitude": -8.65, "longitude": 115.2167 },
        { "name": "Sangereng", "country": "Indonesia", "latitude": -6.2889, "longitude": 106.7181 },
        { "name": "Semarang", "country": "Indonesia", "latitude": -6.9667, "longitude": 110.4167 },
    ]
    # fmt: on

    cities_dfs = []
    for city in cities:
        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "start_date": "2010-01-01",
            "end_date": "2023-06-17",
            "daily": "weathercode,temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,sunrise,sunset,shortwave_radiation_sum,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,et0_fao_evapotranspiration",
            "timezone": "GMT",
            "min": "2010-01-01",
            "max": "2023-06-17",
        }

        print(f"Querying weather API for {city['name']} - {city['country']}...")
        res = requests.get(url, params=params)

        if res.status_code != 200:
            res.raise_for_status()
            raise RuntimeError(
                f"Request to {url} returned status code {res.status_code}"
            )

        data = res.json()

        # Convert data to tabular format and add some metadata
        print("Preprocessing...")
        df = pd.DataFrame(data["daily"])
        df["latitude"] = data["latitude"]
        df["longitude"] = data["longitude"]
        df["elevation"] = data["elevation"]
        df["country"] = city["country"]
        df["city"] = city["name"]

        cities_dfs.append(df)

    concat_df = pd.concat(cities_dfs, ignore_index=True)
    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "weather"
    )
    file_name = "open_meteo_indonesia.csv"

    concat_df.to_csv(data_path / file_name, index=False)


if __name__ == "__main__":
    main()