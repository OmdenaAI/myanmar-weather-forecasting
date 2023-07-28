import streamlit as st
from utils.inference import ENb0, ResNet18
from streamlit_image_select import image_select

st.set_page_config(
    page_title="Omdena Myanmar Local Chapter - Traffic",
    page_icon="src/streamlit/img/favicon.png",
)

# styles
# Streamlit doesn't allow to change the color of the progress bar, so we have to do with CSS
# The idea was to have a blue-red gradient, where the bar was blue if traffic was low and turned red until Traffic Jam
st.markdown(
    """
<style>

    .stProgress {
        transform: scale(-1, 1);
    }
    .stProgress > div > div > div > div {
        background-color: #f0f2f6;
        border-radius: 0;
    }
    .stProgress > div > div > div {
        height: 15px;
        background-image: linear-gradient(0.25turn, red, blue);
        border-radius: 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.header("Traffic Congestion")
st.markdown(
    "We dediced to frame the traffic congestion problem as a computer vision problem."
    " The idea was to work with images of traffic cameras and classify the current"
    ' traffic situation the camera was "seeing". \n\nThe source of data was Kaggle\'s'
    " [Traffic Density"
    " Singapore](https://www.kaggle.com/datasets/rahat52/traffic-density-singapore)"
    " dataset. It contains images from Singapore's [Land Transport"
    " Authority](https://www.lta.gov.sg/) labeled as 5 classes: **Empty**, **Low**,"
    " **Medium**, **High** and **Traffic Jam**"
)

model_map = {"EfficientNet": ENb0, "ResNet": ResNet18}
st.subheader("Choose a model")
st.markdown(
    "Due to the limited resources of Streamlit Could, we had to work with models that"
    " were small in size."
)
option = st.selectbox(
    label="Choose a model",
    options=["EfficientNet", "ResNet"],
    label_visibility="collapsed",
)
st.divider()

st.subheader("Select one of the example images")
sample_img = image_select(
    label="",
    images=[
        "src/streamlit/img/singapore1.jpg",
        "src/streamlit/img/singapore2.jpg",
        "src/streamlit/img/singapore3.jpg",
        "src/streamlit/img/singapore4.jpg",
        "src/streamlit/img/myanmar1.jpg",
        "src/streamlit/img/myanmar2.jpg",
        "src/streamlit/img/myanmar3.jpg",
    ],
    use_container_width=True,
)

st.subheader("or upload one")
st.markdown(
    "Uploaded images take precedence over the example ones. You can grab a real time"
    " image from Singapore's traffic cameras"
    " [here](https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras.html),"
    " but feel free to test the model any other traffic image"
)
uploaded_file = st.file_uploader(
    label="Uploaded images take precedence over the example images",
    accept_multiple_files=False,
    type=["png", "jpg"],
    label_visibility="collapsed",
)
# Values are inverted because of CSS. See #styles above
traffic_map = {"Empty": 100, "Low": 75, "Medium": 50, "High": 25, "Traffic Jam": 0}
predicted_class = None
if uploaded_file is not None:
    st.divider()
    st.subheader("Image preview")
    img_bytes = uploaded_file.read()
    st.image(img_bytes)
    with st.spinner(f"Loading {option}"):
        model = model_map[option]()

    predicted_class = model.inference(img_bytes)

elif sample_img:
    st.divider()
    st.subheader("Image preview")
    st.image(str(sample_img))
    with st.spinner(f"Loading {option}"):
        model = model_map[option]()

    predicted_class = model.inference(sample_img)

if predicted_class is not None:
    st.markdown(f"Traffic class: **{predicted_class}**")
    st.progress(
        traffic_map[predicted_class],
    )
