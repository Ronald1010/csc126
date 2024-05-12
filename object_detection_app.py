import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import io

import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, ClientSettings

weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
categories = weights.meta["categories"] ## ['__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stopsign',]
img_preprocess = weights.transforms() ## Scales values from 0-255 range to 0-1 range.

@st.cache_resource
def load_model():
    model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.5)
    model.eval() ## Setting Model for Evaluation/Prediction   
    return model

model = load_model()

def make_prediction(img): 
    img_processed = img_preprocess(img) ## (3,500,500) 
    prediction = model(img_processed.unsqueeze(0)) # (1,3,500,500)
    prediction = prediction[0]                       ## Dictionary with keys "boxes", "labels", "scores".
    prediction["labels"] = [categories[label] for label in prediction["labels"]]
    return prediction

def create_image_with_bboxes(img, prediction): ## Adds Bounding Boxes around original Image.
    img_tensor = torch.tensor(img) ## Transpose
    img_with_bboxes = draw_bounding_boxes(img_tensor, boxes=prediction["boxes"], labels=prediction["labels"],
                                          colors=["red" if label=="person" else "green" for label in prediction["labels"]] , width=2)
    img_with_bboxes_np = img_with_bboxes.detach().numpy().transpose(1,2,0) ### (3,W,H) -> (W,H,3), Channel first to channel last.
    return img_with_bboxes_np

class VideoTransformer(VideoTransformerBase):
    def __init__(self) -> None:
        self.model = load_model()

    def transform(self, frame):
        # Convert frame to PIL Image
        img = Image.fromarray(frame)
        # Make prediction
        prediction = make_prediction(img)
        # Draw bounding boxes
        img_with_bbox = create_image_with_bboxes(np.array(img).transpose(2,0,1), prediction)
        # Convert image back to numpy array
        img_with_bbox = np.array(img_with_bbox)
        return img_with_bbox

## Dashboard
st.title("CSC126 Project Object Detector")
st.markdown("---")

# File Uploader and Camera Option
option = st.radio("Choose an option:", ("Upload Image", "Use Camera"))

if option == "Upload Image":
    upload = st.file_uploader(label="Upload Image Here:", type=["png", "jpg", "jpeg"])

    if upload:
        img = Image.open(upload)

        prediction = make_prediction(img) ## Dictionary
        img_with_bbox = create_image_with_bboxes(np.array(img).transpose(2,0,1), prediction) ## (W,H,3) -> (3,W,H)

        fig = plt.figure(figsize=(12,12))
        ax = fig.add_subplot(111)
        plt.imshow(img_with_bbox)
        plt.xticks([],[])
        plt.yticks([],[])
        ax.spines[["top", "bottom", "right", "left"]].set_visible(False)

        st.pyplot(fig, use_container_width=True)

        del prediction["boxes"]
        st.header("Predicted Probabilities")
        st.write(prediction)

elif option == "Use Camera":
    st.write("Please click the 'Start' button to use your camera.")
    st.write("(Note: Camera support might not be available on all devices)")

    webrtc_ctx = webrtc_streamer(
        key="example",
        video_transformer_factory=VideoTransformer,
        client_settings=ClientSettings(
            media_stream_constraints={
                "video": True,
            }
        ),
    )
