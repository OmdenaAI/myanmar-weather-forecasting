import streamlit as st
import pandas as pd
import numpy as np
import pathlib
from streamlit_folium import st_folium
from prophet.serialize import model_from_json
import folium
import datetime as dt
from math import cos, asin, sqrt, pi


@st.cache_data
def get_data():
    data_path = pathlib.Path(__file__).parents[3] / "data"
    df = pd.read_csv(data_path / "weather" / "open_meteo.csv")

    city_info_cols = ["city", "country", "latitude", "longitude"]
    # Get unique combinations of city_info_cols
    cities_index = pd.DataFrame(
        df.groupby(city_info_cols).groups.keys(), columns=city_info_cols
    )

    return df, cities_index


@st.cache_data
def get_city_data(city_name, country_name, raw_df):
    return raw_df[(raw_df["city"] == city_name) & (raw_df["country"] == country_name)]


# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371  # km
    p = pi / 180

    a = (
        0.5
        - cos((lat2 - lat1) * p) / 2
        + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    )
    return 2 * r * asin(sqrt(a))


@st.cache_data
def get_nearest_city(lat, lng, cities_df):
    min_ = float("inf")
    closest_city = None

    for _, city, country, latitude, longitude in cities_df.itertuples():
        hav_dist = haversine_distance(lat, lng, latitude, longitude)

        if hav_dist < min_:
            min_ = hav_dist
            closest_city = (city, country, latitude, longitude)

    return closest_city


@st.cache_data
def get_models_for_city(city, country):
    st.write("Fetching models...")
    models = []
    models_dir = (
        pathlib.Path(__file__).parents[3]
        / "models"
        / "weather"
        / country
        / city
        / "prophet"
    )

    for model_path in models_dir.glob("*.json"):
        splitted = model_path.name.split("_")
        train_start = splitted[-2]
        train_end = splitted[-1].removesuffix(".json")
        var_name = "_".join(splitted[:-2])

        with model_path.open("r") as f:
            models.append(
                {
                    "file": model_path.name,
                    "predictor": model_from_json(f.read()),
                    "variable": var_name,
                    "train_start": train_start,
                    "train_end": train_end,
                }
            )

    return models


if "center" not in st.session_state:
    st.session_state["center"] = (9.45, 120.76)


st.header("Weather Forecasting")


df, cities_df = get_data()

m = folium.Map(location=st.session_state["center"], zoom_start=4, tiles="OpenStreetMap")

fg = folium.FeatureGroup(name="markers")

for _, city, country, lat, lng in cities_df.itertuples():
    folium.Circle(
        location=(lat, lng), radius=30000, color="crimson", fill=True, tooltip=city
    ).add_to(fg)

# try to search for map info(sha256) in session_state
lat, lng = None, None
for value in st.session_state.values():
    if isinstance(value, dict) and "last_clicked" in value:
        lat, lng = value["last_clicked"].values()
        fg.add_child(folium.Marker((lat, lng)))
        break

st.subheader("Select a location on the map")

map_data = st_folium(
    m,
    use_container_width=True,
    height=500,
    feature_group_to_add=fg,
    returned_objects=["last_clicked"],
)

if lat is not None and lng is not None:
    st.write(f"Selected location: Lat: {lat} Lng: {lng}")

    city, country, *_ = get_nearest_city(lat, lng, cities_df)
    st.write(f"The nearest city is {city} - {country}")

    date_container = st.container()
    graphs_container = st.container()

    date_container.date_input(
        "Select the period you wish to know the forecast for",
        key="date_input",
        value=(dt.datetime.today(), dt.datetime.today() + dt.timedelta(days=30)),
        min_value=dt.datetime(year=2021, month=1, day=1),
    )

    st.session_state["models"] = get_models_for_city(city, country)
    # st.write(st.session_state)

    if "date_input" not in st.session_state or len(st.session_state["date_input"]) < 2:
        pass

    else:
        for model_info in st.session_state["models"]:
            st.subheader(f"Forecasting {model_info['variable']} from scratch")
            train_end = dt.datetime.strptime(
                model_info["train_end"], "%Y-%m-%d %H:%M:%S"
            ).date()

            period_start = st.session_state["date_input"][0]
            period_end = st.session_state["date_input"][1]

            days_to_predict = (period_end - train_end).days
            days_to_show = (period_end - period_start).days

            future = model_info["predictor"].make_future_dataframe(
                periods=days_to_predict
            )
            st.line_chart(
                data=model_info["predictor"].predict(future).iloc[-days_to_show:],
                x="ds",
                y="yhat",
                use_container_width=True,
            )
