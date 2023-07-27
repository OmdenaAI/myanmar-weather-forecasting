import streamlit as st
from utils.inference import ENb0, ResNet18
from streamlit_image_select import image_select

st.set_page_config(
    page_title="Omdena Myanmar Local Chapter - Traffic",
    page_icon="src/streamlit/img/favicon.png",
)

st.header("Traffic Congestion")

model_map = {"EfficientNet": ENb0, "ResNet": ResNet18}
st.subheader("Choose a model")
option = st.selectbox(
    label="Choose a model",
    options=["EfficientNet", "ResNet"],
    label_visibility="collapsed",
)
st.divider()

st.subheader("Upload an image of traffic to classify")
uploaded_file = st.file_uploader(
    label="Upload an image of traffic to get a classification",
    accept_multiple_files=False,
    type=["png", "jpg"],
    label_visibility="collapsed",
)
st.subheader("Or select one of the template images")
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
traffic_map = {"Empty": 0, "Low": 25, "Medium": 50, "High": 75, "Traffic Jam": 100}
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
    st.write(f"Predicted traffic class: {predicted_class}")
    st.progress(
        traffic_map[predicted_class],
    )
