import streamlit as st
import pandas as pd
import numpy as np
import pathlib
from streamlit_folium import st_folium
import folium
from math import cos, asin, sqrt, pi


@st.cache_data
def get_data():
    data_path = pathlib.Path(__file__).parents[3] / "data"

    return pd.read_csv(data_path / "weather" / "open_meteo.csv")


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


if "center" not in st.session_state:
    st.session_state["center"] = (9.45, 120.76)


st.header("Weather Forecasting")


df = get_data()

cities_df = (
    df.groupby(["city", "country", "latitude", "longitude"])
    .count()
    .reset_index()[["city", "country", "latitude", "longitude"]]
)

m = folium.Map(location=st.session_state["center"], zoom_start=4, tiles="OpenStreetMap")

fg = folium.FeatureGroup(name="markers")

for _, city, country, lat, lng in cities_df.itertuples():
    folium.Circle(
        location=(lat, lng), radius=30000, color="crimson", fill=True, tooltip=city
    ).add_to(fg)

# try to search for map info(sha256) in session_state
lat, lng = None, None
for value in st.session_state.values():
    if "last_clicked" in value:
        lat, lng = value["last_clicked"].values()
        fg.add_child(folium.Marker((lat, lng)))

st.write(st.session_state)

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

    st.write("Fetching data")

    city_df = get_city_data(city, country, df)
    st.dataframe(city_df)

    st.header("Visualizations")
