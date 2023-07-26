import streamlit as st
import pathlib
from utils.inference import ENb0, ResNet18
from streamlit_image_select import image_select

repository_root = pathlib.Path(__file__).parents[3]
img_folder = repository_root / "src" / "streamlit" / "img"
st.header("Traffic Congestion")

model_map = {"EfficientNet": ENb0, "ResNet": ResNet18}
st.write("Choose a model")
option = st.selectbox(
    label="Choose a model",
    options=["EfficientNet", "ResNet"],
    label_visibility="collapsed",
)

st.write("Upload an image of traffic to classify")
uploaded_file = st.file_uploader(
    label="Upload an image of traffic to get a classification",
    accept_multiple_files=False,
    type=["png", "jpg"],
    label_visibility="collapsed",
)
st.write("Or select one of the template images")
sample_img = image_select(
    label="",
    images=[
        img_folder / "low.jpg",
        img_folder / "medium.jpg",
        img_folder / "jam1.jpg",
        img_folder / "jam2.jpg",
    ],
    captions=["Low traffic", "Medium traffic", "Traffic Jam", "Challenging image"],
    use_container_width=True,
)
if uploaded_file is not None:
    img_bytes = uploaded_file.read()
    st.write("Image preview")
    st.image(img_bytes)
    with st.spinner(f"Loading {option}"):
        model = model_map[option]()
    st.write(model.inference(img_bytes))

elif sample_img:
    st.write("Image preview")
    st.image(str(sample_img))
    with st.spinner(f"Loading {option}"):
        model = model_map[option]()
    st.write(model.inference(sample_img))
