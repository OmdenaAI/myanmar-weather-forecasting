# Weather Forecasting and Reducing Traffic Congestion in Southeast Asia Using Machine Learning

## Weather Forecasting
The problem is the occurrence of extreme weather events, such as heatwaves and cold spells especially heatwaves, in Southeast Asian countries. These events have severe consequences, including loss of life due to heat-related illnesses. 
The challenge lies in accurately forecasting these extreme weather conditions to proactively mitigate risks and enable individuals and communities to make informed decisions for their safety and well-being. 
Machine learning can be used to analyze and forecasting the next 30 days. 

## Traffic Congestion
The problem is the prevalence of traffic congestion in Southeast Asian countries, leading to negative impacts such as increased travel time, economic losses, and environmental pollution. The rapid urbanization, population growth, and expanding vehicle ownership exacerbate this issue. 
The challenge is to find effective strategies to reduce traffic congestion, improve transportation efficiency, and enhance the overall quality of life for individuals. This requires collaboration with relevant authorities and stakeholders to identify congestion hotspots and implement targeted interventions. 
Machine learning can be used to analyze the traffic patterns and real-time inputs to predict traffic flow.

## Streamlit web app
Visit the web app [here](https://myanmar-weather-forecasting.streamlit.app/)


https://github.com/OmdenaAI/myanmar-weather-forecasting/assets/32521936/d940f661-f91b-40a6-8031-4891416c9c63



https://github.com/OmdenaAI/myanmar-weather-forecasting/assets/32521936/898ea697-dfc9-41d6-acc0-ed3924d37073




# Contribution Guidelines
- Have a Look at the [project structure](#project-structure) below to understand where to store/upload your contribution
- If you're creating a task, Go to the task folder and create a new folder with the below naming convention and add a README.md with task details and goals to help other contributors understand
    - Task Folder Naming Convention : _task-n-taskname.(n is the task number)_  ex: task-1-data-analysis, task-2-model-deployment etc.
    - Create a README.md with a table containing information table about all contributions for the task.
- If you're contributing for a task, please make sure to store in relavant location and update the README.md information table with your contribution details.
- Make sure your File names(jupyter notebooks, python files, data sheet file names etc) has proper naming to help others in easily identifing them.
- Please restrict yourself from creating unnecessary folders other than in 'tasks' folder (as above mentioned naming convention) to avoid confusion. 

# Project Structure

    ├── LICENSE
    ├── README.md              <- The top-level README for developers/collaborators using this project.
    │
    ├── data                   <- Datasets used and collected for this project
    │   ├── weather
    │   └── traffic
    │   
    ├── tasks                  <- Information on the project's tasks and meeting minutes
    │
    └── src                    <- Source code folder for this project
        └── weather|traffic
            ├── data           <- Scripts to download or generate data
            │
            ├── models         <- Scripts to train models and then use trained models to make predictions
            │
            └── visualization  <- Code and Visualization dashboards generated for the project
--------
