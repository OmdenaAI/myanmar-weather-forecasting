import streamlit as st
import pandas as pd
import pathlib

st.set_page_config(
    page_title="Omdena Myanmar Local Chapter", page_icon="src/streamlit/img/favicon.png"
)
st.header("_The Problem_")
st.markdown(
    ":red[Weather Forecasting]: The problem is the occurrence of extreme weather"
    " events, such as heatwaves and cold spells especially heatwaves, in Southeast"
    " Asian countries. These events have severe consequences, including loss of life"
    " due to heat-related illnesses. The challenge lies in accurately forecasting these"
    " extreme weather conditions to proactively mitigate risks and enable individuals"
    " and communities to make informed decisions for their safety and well-being."
    " Machine learning can be used to analyze and forecasting the next 30 days. "
)
st.markdown(
    ":red[Traffic Congestion]: The problem is the prevalence of traffic congestion in"
    " Southeast Asian countries, leading to negative impacts such as increased travel"
    " time, economic losses, and environmental pollution. The rapid urbanization,"
    " population growth, and expanding vehicle ownership exacerbate this issue. The"
    " challenge is to find effective strategies to reduce traffic congestion, improve"
    " transportation efficiency, and enhance the overall quality of life for"
    " individuals. This requires collaboration with relevant authorities and"
    " stakeholders to identify congestion hotspots and implement targeted"
    " interventions. Machine learning can be used to analyze the traffic patterns and"
    " real-time inputs to predict traffic flow."
)
st.header("_Project Goals_")
st.markdown(
    '<h3 style="font-size: 20px; color: red;">Weather Forecasting:</h3>',
    unsafe_allow_html=True,
)

st.markdown(
    "•  Develop an advanced weather forecasting system specifically tailored to"
    " Myanmar, Philippines and Indonesia."
)
st.markdown(
    "•  Improve the accuracy of weather predictions for extreme weather events like"
    " heatwaves and cold spells."
)
st.markdown(
    "•	Enable individuals and communities to make informed decisions and take proactive"
    " measures to protect themselves during extreme weather conditions."
)
st.markdown(
    "•	Enhance the resilience of communities by providing reliable and timely weather"
    " forecasts."
)
st.markdown(
    "•	Contribute to the reduction of heat-related illnesses and other negative impacts"
    " caused by extreme weather events."
)
st.markdown(
    '<h3 style="font-size: 20px; color: red;">Traffic Congestion:</h3>',
    unsafe_allow_html=True,
)
st.markdown(
    "•	Implement innovative strategies to reduce traffic congestion in Singapore."
)
st.markdown(
    "•	Collaborate with transportation authorities, urban planners, and community"
    " stakeholders to identify congestion hotspots and develop targeted interventions."
)
st.markdown(
    "•	Implement intelligent transportation systems to enhance transportation"
    " efficiency."
)
st.markdown(
    "•	Improve the quality of life for individuals by reducing travel time and enhancing"
    " mobility."
)
