import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
st.title('Forecasting The Weather & Traffic Congestion')

selected = option_menu(menu_title=None,options=['Home','Forecasting The Weather','Reduce Traffic Congestion','About'], 
icons=['house','cloud-moon','stoplights','book'],orientation='horizontal',)
if selected == 'Home':
    st.header('_The Problem_')
    st.markdown(':red[Weather Forecasting]: The problem is the occurrence of extreme weather events, such as heatwaves and cold spells especially heatwaves, in Myanmar. These events have severe consequences, including loss of life due to heat-related illnesses. The challenge lies in accurately forecasting these extreme weather conditions to proactively mitigate risks and enable individuals and communities to make informed decisions for their safety and well-being. Machine learning can be used to analyze and forecasting the next 30 days. ')
    st.markdown(':red[Traffic Congestion]: The problem is the prevalence of traffic congestion in Singapore, leading to negative impacts such as increased travel time, economic losses, and environmental pollution. The rapid urbanization, population growth, and expanding vehicle ownership exacerbate this issue. The challenge is to find effective strategies to reduce traffic congestion, improve transportation efficiency, and enhance the overall quality of life for individuals. This requires collaboration with relevant authorities and stakeholders to identify congestion hotspots and implement targeted interventions. Machine learning can be used to analyze the traffic patterns and real-time inputs to predict traffic flow.')
    st.header('_Project Goals_')
    st.markdown('<h3 style="font-size: 20px; color: red;">Weather Forecasting:</h3>', unsafe_allow_html=True)

    st.markdown('•  Develop an advanced weather forecasting system specifically tailored to Myanmar.')
    st.markdown('•  Improve the accuracy of weather predictions for extreme weather events like heatwaves and cold spells.')
    st.markdown('•	Enable individuals and communities to make informed decisions and take proactive measures to protect themselves during extreme weather conditions.')
    st.markdown('•	Enhance the resilience of communities by providing reliable and timely weather forecasts.')
    st.markdown('•	Contribute to the reduction of heat-related illnesses and other negative impacts caused by extreme weather events.')
    st.markdown('<h3 style="font-size: 20px; color: red;">Traffic Congestion:</h3>', unsafe_allow_html=True)
    st.markdown('•	Implement innovative strategies to reduce traffic congestion in Singapore.')
    st.markdown('•	Collaborate with transportation authorities, urban planners, and community stakeholders to identify congestion hotspots and develop targeted interventions.')
    st.markdown('•	Implement intelligent transportation systems to enhance transportation efficiency.')
    st.markdown('•	Improve the quality of life for individuals by reducing travel time and enhancing mobility.')
elif selected == 'About':
    st.header('_Project Background_')
    st.image('tasks/task-5-deployment/Bagan-Temples.jpg')

    st.markdown('Extreme weather events in Myanmar, including heatwaves. They have resulted in severe consequences, including loss of life due to heat-related illnesses. Accurate weather forecasting is crucial for proactive risk mitigation. :red[This project aims to develop an advanced weather forecasting system using historical data, and machine learning algorithms to enhance predictions, protect lives, and build community resilience.]')
    st.image('tasks/task-5-deployment/images (1).jpeg',width=700)
    st.markdown('Traffic congestion is a pressing issue in Singapore, leading to increased travel time, economic losses, and environmental pollution. This project focuses on reducing congestion by implementing innovative strategies and collaborating with transportation authorities, urban planners, and community stakeholders. :red[Our interventions include seeing so many cars that we can identify that this traffic is jammed.] By alleviating congestion, we aim to improve quality of life, enhance productivity, reduce emissions, and foster sustainable transportation systems.')
    
elif selected == 'Forecasting The Weather':
    st.header("_Forecasting the Myanmar Weather_")
    model = pd.read_pickle("yangoon_windspeed_forecast.pkl")
    date = st.text_input('Date')
    ws = st.text_input('Wind Speed')
    df = pd.DataFrame({"ds":[date],'y':[ws]})
    st.write(model.predict(df))
elif selected == 'Reduce Traffic Congestion':
    st.header("_Traffic Congestion of Singapore_")
