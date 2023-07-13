import requests
import pathlib
import pandas as pd


def main():
    url = "https://archive-api.open-meteo.com/v1/archive"
    # fmt: off
    cities = [
        { "name": "Yangoon", "country": "Myanmar", "latitude": 16.795, "longitude": 96.16 },
        { "name": "Mandalay", "country": "Myanmar", "latitude": 21.9831, "longitude": 96.0844 },
        { "name": "Nay Pyi Taw", "country": "Myanmar", "latitude": 19.7475, "longitude": 96.115 },
        { "name": "Hpa-An", "country": "Myanmar", "latitude": 16.8906, "longitude": 97.6333 },
        { "name": "Maungdaw", "country": "Myanmar", "latitude": 20.8167, "longitude": 92.3667 },
        { "name": "Taunggyi", "country": "Myanmar", "latitude": 20.7836, "longitude": 97.0354 },
        { "name": "Magway", "country": "Myanmar", "latitude": 20.15, "longitude": 94.95 },
        { "name": "Myeik", "country": "Myanmar", "latitude": 12.4333, "longitude": 98.6 },
        { "name": "Keng Tung", "country": "Myanmar", "latitude": 21.2827, "longitude": 99.623 },
        { "name": "Laukkaing", "country": "Myanmar", "latitude": 23.6872, "longitude": 98.7646 },
        { "name": "Medan", "country": "Indonesia", "latitude": 3.59, "longitude": 98.678  },
        { "name": "Pekanbaru", "country": "Indonesia", "latitude": 0.526, "longitude": 101.45 },
        { "name": "Palembang", "country": "Indonesia", "latitude": -2.987, "longitude": 104.76 },
        { "name": "Jakarta", "country": "Indonesia", "latitude": -6.175, "longitude": 106.865 },
        { "name": "Pontianak", "country": "Indonesia", "latitude": -0.021, "longitude": 109.336 },
        { "name": "Surabaya", "country": "Indonesia", "latitude": -7.245, "longitude": 112.737 },
        { "name": "Balikpapan", "country": "Indonesia", "latitude": -1.239, "longitude": 116.859 },
        { "name": "Makassar", "country": "Indonesia", "latitude": -5.134, "longitude": 119.412 },
        { "name": "Manado", "country": "Indonesia", "latitude": 1.49, "longitude": 124.84 },
        { "name": "Sorong", "country": "Indonesia", "latitude": -0.863, "longitude": 131.254 },
        { "name": "Manila", "country": "Philippines", "latitude": 14.5958, "longitude": 120.9772 },
        { "name": "Baguio", "country": "Philippines", "latitude": 16.4119, "longitude": 120.5933 },
        { "name": "Tuguegarao", "country": "Philippines", "latitude": 17.6133, "longitude": 121.7303 },
        { "name": "Legazpi", "country": "Philippines", "latitude": 13.13, "longitude": 123.73 },
        { "name": "Iloilo", "country": "Philippines", "latitude": 10.72, "longitude": 122.57 },
        { "name": "Tacloban", "country": "Philippines", "latitude": 11.24, "longitude": 125 },
        { "name": "Pagadian", "country": "Philippines", "latitude": 7.8272, "longitude": 123.4364 },
        { "name": "Davao", "country": "Philippines", "latitude": 7.07, "longitude": 125.6 },
        { "name": "Butuan", "country": "Philippines", "latitude": 8.95, "longitude": 125.53 },
        { "name": "Puerto Princesa", "country": "Philippines", "latitude": 9.75, "longitude": 118.75 },
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
    file_name = "open_meteo.csv"

    concat_df.to_csv(data_path / file_name, index=False)


if __name__ == "__main__":
    main()
