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


st.set_page_config(
    page_title="Omdena Myanmar Local Chapter - Weather",
    page_icon="src/streamlit/img/favicon.png",
)


st.header("Weather Forecasting")
st.markdown(
    "To tackle the weather forecasting problem, we used [open-meteo's Historical"
    " Weather API](https://open-meteo.com/en/docs/historical-weather-api) to collect"
    " data from cities in the Southeast Asia region with a focus on the following"
    " countries: **Myanmar**, **Indonesia** and **Philippines**."
)

st.markdown(
    (
        "We're able to collect historical infomation like temperature, wind speed and"
        " rain - some of the most straightforward indicators of dangerous weather"
        " events - to build our models."
    ),
    unsafe_allow_html=True,
)


df, cities_df = get_data()

# (9.45, 120.76) are the coordinates of somewhere in the center of SEA
m = folium.Map(location=(9.45, 120.76), zoom_start=4, tiles="OpenStreetMap")

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

st.subheader("Select a location")
st.markdown(
    "Weather can vary wildly, even within the same country. Click on the map to select"
    " the location you're interested in knowing the forecast for."
)
st.caption("Red dots represent the locations we have data on")

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

    st.subheader("Select a period")
    st.write(
        "Use the calendar widget to select a range (start and end dates). You'll be"
        " given the model's forecast for that period of time."
    )
    st.caption(
        "Extremely long ranges (spanning over multiple years) may be slow to load and"
        " give out weird results"
    )
    st.date_input(
        label="Select the period you wish to know the forecast for",
        key="date_input",
        value=(dt.datetime.today(), dt.datetime.today() + dt.timedelta(weeks=24)),
        min_value=dt.datetime(year=2021, month=1, day=1),
        label_visibility="collapsed",
    )

    with st.spinner("Fetching models..."):
        st.session_state["models"] = get_models_for_city(city, country)

    if "date_input" in st.session_state and len(st.session_state["date_input"]) >= 2:
        var_info = {
            "temperature_2m_min": "Temperature",
            "temperature_2m_max": "Temperature",
            "temperature_2m_mean": "Temperature",
            "rain_sum": "Rain",
            "windspeed_10m_max": "Wind speed",
        }
        group_info = {
            "Temperature": "°C",
            "Rain": "mm",
            "Wind speed": "km/h",
        }

        charts_data = {}
        with st.spinner("Running prediction models..."):
            for model_info in st.session_state["models"]:
                current_var = model_info["variable"]
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

                predictions = (
                    model_info["predictor"].predict(future).iloc[-days_to_show:]
                )

                if var_info[current_var] == "Temperature":
                    if "Temperature" not in charts_data:
                        charts_data["Temperature"] = [predictions["ds"]]

                    charts_data["Temperature"].append(
                        predictions["yhat"].rename(current_var.split("_")[-1])
                    )
                    continue

                charts_data[var_info[current_var]] = [predictions]

        # plotting charts
        for group, predictions in charts_data.items():
            st.subheader(f"{group}")

            if group == "Temperature":
                chart_data = pd.concat(
                    predictions,
                    axis="columns",
                ).melt(id_vars="ds", var_name="Temperature", value_name="yhat")

                line = (
                    alt.Chart(chart_data)
                    .mark_line()
                    .encode(
                        x=alt.X("ds").title("Date"),
                        y=alt.Y("yhat").title(f"{group} ({group_info[group]})"),
                        color=alt.Color(
                            "Temperature",
                            scale=alt.Scale(
                                domain=["max", "mean", "min"],
                                range=["#f96d6d", "#add8fe", "#5694d7"],
                            ),
                            legend=alt.Legend(orient="top"),
                        ),
                    )
                )

            elif group == "Wind speed":
                [chart_data] = predictions
                # main line
                line = (
                    alt.Chart(chart_data)
                    .mark_line()
                    .encode(
                        x=alt.X("ds").title("Date"),
                        y=alt.Y("yhat").title(f"{group} ({group_info[group]})"),
                    )
                )

            elif group == "Rain":
                [chart_data] = predictions
                # main line
                line = (
                    alt.Chart(chart_data)
                    .mark_line()
                    .encode(
                        x=alt.X("ds").title("Date"),
                        y=alt.Y("yhat").title(f"{group} ({group_info[group]})"),
                    )
                )

            hover = alt.selection_single(
                fields=["ds"],
                nearest=True,
                on="mouseover",
                empty="none",
            )

            # make points on the line on hover
            points = line.transform_filter(hover).mark_circle(size=65)

            # vertical line and tooltip
            tooltips = (
                alt.Chart(chart_data)
                .mark_rule()
                .encode(
                    x="ds",
                    y="yhat",
                    opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                    tooltip=[
                        alt.Tooltip("ds", title="Date"),
                        alt.Tooltip(
                            "yhat",
                            title=f"{group} ({group_info[group]})",
                        ),
                    ],
                )
                .add_selection(hover)
            )

            st.altair_chart(
                (line + points + tooltips).interactive(),
                use_container_width=True,
                theme="streamlit",
            )
