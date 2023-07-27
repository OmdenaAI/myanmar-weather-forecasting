import streamlit as st
import pandas as pd
import numpy as np
import pathlib
from streamlit_folium import st_folium
from prophet.serialize import model_from_json
import folium
import datetime as dt
import altair as alt
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
            closest_city = (city, country, latitude, longitude, hav_dist)

    return closest_city


@st.cache_data
def get_models_for_city(city, country):
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

st.set_page_config(
    page_title="Omdena Myanmar Local Chapter - Weather",
    page_icon="src/streamlit/img/favicon.png",
)


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
    city, country, *_, distance_km = get_nearest_city(lat, lng, cities_df)
    lat_col, lng_col, city_col, distance_col = st.columns(4)

    lat_col.metric(
        label="Latitude", value=f"{lat:.2f}", help="Latitude in decimal degrees"
    )
    lng_col.metric(
        label="Longitude", value=f"{lng:.2f}", help="Longitude in decimal degrees"
    )
    city_col.metric(
        label="Nearest city",
        value=f"{city}",
        help="Source of the data we'll be using for the prediction",
    )

    distance_col.metric(
        label="Distance",
        value=f"{distance_km:.2f} Km",
        help="Distance in Km from nearest city to marker on the map",
    )

    if distance_km > 400:
        st.warning(
            "Selected location is far from any of the reference cities. This may result"
            " in a worse forecast"
        )

    st.subheader("Range to forecast")
    st.date_input(
        label="Select the period you wish to know the forecast for",
        key="date_input",
        value=(dt.datetime.today(), dt.datetime.today() + dt.timedelta(days=30)),
        min_value=dt.datetime(year=2021, month=1, day=1),
        label_visibility="collapsed",
    )

    with st.spinner("Fetching models..."):
        st.session_state["models"] = get_models_for_city(city, country)

    if "date_input" in st.session_state and len(st.session_state["date_input"]) >= 2:
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

            chart_data = model_info["predictor"].predict(future).iloc[-days_to_show:]
            line = (
                alt.Chart(chart_data)
                .mark_line()
                .encode(
                    x=alt.X("ds").title("Date"),
                    y=alt.Y("yhat").title(model_info["variable"]),
                )
            )

            hover = alt.selection_single(
                fields=["ds"],
                nearest=True,
                on="mouseover",
                empty="none",
            )

            points = line.transform_filter(hover).mark_circle(size=65)

            tooltips = (
                alt.Chart(chart_data)
                .mark_rule()
                .encode(
                    x="ds",
                    y="yhat",
                    opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                    tooltip=[
                        alt.Tooltip("ds", title="Date"),
                        alt.Tooltip("yhat", title=model_info["variable"]),
                    ],
                )
                .add_selection(hover)
            )
            st.altair_chart(
                (line + points + tooltips).interactive(),
                use_container_width=True,
                theme="streamlit",
            )
