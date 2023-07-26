import pandas as pd
import numpy as np
import pathlib
from prophet import Prophet
from prophet.serialize import model_to_json


def main():
    data_path = pathlib.Path(__file__).parents[3] / "data" / "weather"
    save_dir = pathlib.Path(__file__).parents[3] / "models" / "weather"

    full_df = pd.read_csv(data_path / "open_meteo.csv")
    full_df["time"] = pd.to_datetime(full_df["time"])

    city_info_cols = ["city", "country", "latitude", "longitude"]
    # Get unique combinations of city_info_cols
    cities_index = pd.DataFrame(
        full_df.groupby(city_info_cols).groups.keys(), columns=city_info_cols
    )

    variables_to_predict = (
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "rain_sum",
        "windspeed_10m_max",
    )

    for _, city, country, *_ in cities_index.itertuples():
        df = full_df[(full_df["city"] == city) & (full_df["country"] == country)]

        train_df_multivar = df.loc[df["time"].dt.year < 2021]
        test_df_multivar = df.loc[df["time"].dt.year >= 2021]

        for var in variables_to_predict:
            train_df = train_df_multivar[["time", var]].rename(
                columns={"time": "ds", var: "y"}
            )
            test_df = test_df_multivar[["time", var]].rename(
                columns={"time": "ds", var: "y"}
            )

            print(f"Training {var} forecasting model for {city}-{country}")
            model = Prophet(yearly_seasonality=20)
            model.fit(train_df)
            future = model.make_future_dataframe(periods=len(test_df))
            preds = model.predict(future)

            rmse = np.sqrt(
                np.mean(
                    (test_df["y"].values - preds["yhat"].tail(len(test_df)).values) ** 2
                )
            )
            print(f"Test RMSE: {rmse:03}")

            model_name = (
                f"{var}_{train_df['ds'].iloc[0]}_{train_df['ds'].iloc[-1]}.json"
            )
            save_path = save_dir / country / city / "prophet" / model_name
            save_path.parent.mkdir(exist_ok=True, parents=True)

            print(f"Saving model as {model_name} ...")
            with save_path.open("w") as f:
                f.write(model_to_json(model))


if __name__ == "__main__":
    main()
