import streamlit as st
from streamlit_option_menu import option_menu
st.title('Forecasting The Weather & Traffic Congestion')

selected = option_menu(menu_title=None,options=['Home','Forecasting The Weather','Reduce Traffic Congestion','About'], 
icons=['house','cloud-moon','stoplights','book'],orientation='horizontal',)
if selected == 'Home':
    st.header('_The Problem_')
    st.markdown(':red[Weather Forecasting]: The problem is the occurrence of extreme weather events, such as heatwaves and cold spells especially heatwaves, in Southeast Asian countries. These events have severe consequences, including loss of life due to heat-related illnesses. The challenge lies in accurately forecasting these extreme weather conditions to proactively mitigate risks and enable individuals and communities to make informed decisions for their safety and well-being. Machine learning can be used to analyze and forecasting the next 30 days. ')
    st.markdown(':red[Traffic Congestion]: The problem is the prevalence of traffic congestion in Southeast Asian countries, leading to negative impacts such as increased travel time, economic losses, and environmental pollution. The rapid urbanization, population growth, and expanding vehicle ownership exacerbate this issue. The challenge is to find effective strategies to reduce traffic congestion, improve transportation efficiency, and enhance the overall quality of life for individuals. This requires collaboration with relevant authorities and stakeholders to identify congestion hotspots and implement targeted interventions. Machine learning can be used to analyze the traffic patterns and real-time inputs to predict traffic flow.')
    st.header('_Project Goals_')
    st.markdown('<h3 style="font-size: 20px; color: red;">Weather Forecasting:</h3>', unsafe_allow_html=True)

    st.markdown('•  Develop an advanced weather forecasting system specifically tailored to Myanmar, Philippines and Indonesia.')
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
    image = 'myanmar.jpg'
    st.image(image, use_column_width=True)
    st.markdown('Extreme weather events in Southeast Asian countries, including heatwaves. They have resulted in severe consequences, including loss of life due to heat-related illnesses. Accurate weather forecasting is crucial for proactive risk mitigation. This project aims to develop an advanced weather forecasting system using meteorological data, and machine learning algorithms to enhance predictions, protect lives, and build community resilience.')
    st.markdown('Traffic congestion is a pressing issue in Southeast Asian countries, leading to increased travel time, economic losses, and environmental pollution. This project focuses on reducing congestion by implementing innovative strategies and collaborating with transportation authorities, urban planners, and community stakeholders. Our interventions include optimizing traffic signal timing, implementing intelligent transportation systems, promoting alternative transportation modes, and encouraging carpooling. By alleviating congestion, we aim to improve quality of life, enhance productivity, reduce emissions, and foster sustainable transportation systems.')
    
elif selected == 'Forecasting The Weather':
    country = st.radio("Choose Country:",('Myanmar','Philippines','Indonesia'))