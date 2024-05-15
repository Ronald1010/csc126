<<<<<<< HEAD
import streamlit as st
from PIL import Image
from inference_sdk import InferenceHTTPClient
import tempfile
import requests

# Define the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="VsxreoZsgrCDLK4xweXv"
)

MODEL_ID = "diabetic-retinopathy-mnthr/2"

def infer_image(image):
    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        image.save(temp_file, format='JPEG')
        temp_file_path = temp_file.name
    
    # Use the inference client to send the image
    result = CLIENT.infer(temp_file_path, model_id=MODEL_ID)
    return result

# Define descriptions and advice for each class
CLASS_DESCRIPTIONS = {
    "Proliferate_DR": {
        "description": "Proliferative diabetic retinopathy detected.",
        "advice": "Urgently consult with an eye specialist for prompt treatment to prevent vision loss."
    },
    "Severe": {
        "description": "Severe diabetic retinopathy detected.",
        "advice": "Seek immediate medical attention from an eye specialist for appropriate treatment."
    },
    "Unlabeled": {
        "description": "Unlabeled.",
        "advice": "This class is not labeled. Please consult with a healthcare professional for further evaluation."
    },
    "mild": {
        "description": "Mild diabetic retinopathy detected.",
        "advice": "Control blood sugar levels and maintain a healthy lifestyle. Regular eye check-ups are recommended."
    },
    "moderate": {
        "description": "Moderate diabetic retinopathy detected.",
        "advice": "Consult with an eye specialist for further evaluation and treatment options."
    },
    "no_DR": {
        "description": "No signs of diabetic retinopathy detected.",
        "advice": "Continue regular eye check-ups as advised by your healthcare provider."
    }
}

# Streamlit app
st.set_page_config(page_title="Diabetic Retinal Disease Detection", page_icon="👁️", layout="centered")
st.title("👁️ Diabetic Retinal Disease Detection App")

# Apply CSS styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
        padding: 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.subheader("Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Displaying preloader while detecting diabetic retinal disease
    with st.spinner("Detecting diabetic retinal disease..."):
        result = infer_image(image)

    # Display results after preloader
    if result and "predictions" in result:
        st.subheader("Detection Result")
        predictions = result["predictions"]
        max_prediction = max(predictions.items(), key=lambda x: x[1]['confidence'])
        class_name, prediction = max_prediction
        confidence = prediction['confidence']
        
        # Set background color based on predicted class
        if class_name == "no_DR":
            background_color = "#57BB8A"
        elif class_name == "mild":
            background_color = "#F8D347"
        else:
            background_color = "#F24236"
        
        # Apply background color
        st.markdown(
            f"""
            <div style='background-color: {background_color}; padding: 1rem; border-radius: 0.5rem;'>
                <h3 style='color: white;'>Detection Result</h3>
                <p style='color: white;'>Predicted Class: {class_name.capitalize()} ({confidence:.2%})</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        description = CLASS_DESCRIPTIONS.get(class_name, {}).get("description", "")
        advice = CLASS_DESCRIPTIONS.get(class_name, {}).get("advice", "")

        # Display description and advice based on predicted class
        st.write(description)
        st.write(f"**Advice:** {advice}")

        # Display annotated image
        annotated_image_url = result.get("annotated_image")
        if annotated_image_url:
            annotated_image = Image.open(requests.get(annotated_image_url, stream=True).raw)
            st.subheader("Annotated Image")
            st.image(annotated_image, caption='Annotated Image', use_column_width=True)
    else:
        st.markdown('<p style="color: green; font-weight: bold;">No signs of diabetic retinal disease detected.</p>', unsafe_allow_html=True)
=======
import streamlit as st
from PIL import Image
from inference_sdk import InferenceHTTPClient
import tempfile
import requests
from typing import Iterable

# Define the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="VsxreoZsgrCDLK4xweXv"
)

MODEL_ID = "diabetic-retinopathy-mnthr/2"

def infer_image(image):
    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        image.save(temp_file, format='JPEG')
        temp_file_path = temp_file.name
    
    # Use the inference client to send the image
    result = CLIENT.infer(temp_file_path, model_id=MODEL_ID)
    return result

# Define descriptions and advice for each class
CLASS_DESCRIPTIONS = {
    "Proliferate_DR": {
        "description": "Proliferative diabetic retinopathy detected.",
        "advice": "Urgently consult with an eye specialist for prompt treatment to prevent vision loss."
    },
    "Severe": {
        "description": "Severe diabetic retinopathy detected.",
        "advice": "Seek immediate medical attention from an eye specialist for appropriate treatment."
    },
    "Unlabeled": {
        "description": "Unlabeled.",
        "advice": "This class is not labeled. Please consult with a healthcare professional for further evaluation."
    },
    "mild": {
        "description": "Mild diabetic retinopathy detected.",
        "advice": "Control blood sugar levels and maintain a healthy lifestyle. Regular eye check-ups are recommended."
    },
    "moderate": {
        "description": "Moderate diabetic retinopathy detected.",
        "advice": "Consult with an eye specialist for further evaluation and treatment options."
    },
    "no_DR": {
        "description": "No signs of diabetic retinopathy detected.",
        "advice": "Continue regular eye check-ups as advised by your healthcare provider."
    }
}

# Streamlit app
st.set_page_config(page_title="Diabetic Retinal Disease Detection", page_icon="👁️", layout="centered")
st.title("👁️ Diabetic Retinal Disease Detection App")

# Apply CSS styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
        padding: 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.subheader("Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Displaying preloader while detecting diabetic retinal disease
    with st.spinner("Detecting diabetic retinal disease..."):
        result = infer_image(image)

    # Display results after preloader
    if result and "predictions" in result:
        st.subheader("Detection Result")
        predictions = result["predictions"]
        max_prediction = max(predictions.items(), key=lambda x: x[1]['confidence'])
        class_name, prediction = max_prediction
        confidence = prediction['confidence']
        
        # Set background color based on predicted class
        if class_name == "no_DR":
            background_color = "#57BB8A"
        elif class_name == "mild":
            background_color = "#F8D347"
        else:
            background_color = "#F24236"
        
        # Apply background color
        st.markdown(
            f"""
            <div style='background-color: {background_color}; padding: 1rem; border-radius: 0.5rem;'>
                <h3 style='color: white;'>Detection Result</h3>
                <p style='color: white;'>Predicted Class: {class_name.capitalize()} ({confidence:.2%})</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        description = CLASS_DESCRIPTIONS.get(class_name, {}).get("description", "")
        advice = CLASS_DESCRIPTIONS.get(class_name, {}).get("advice", "")

        # Display description and advice based on predicted class
        st.write(description)
        st.write(f"**Advice:** {advice}")

        # Display annotated image
        annotated_image_url = result.get("annotated_image")
        if annotated_image_url:
            annotated_image = Image.open(requests.get(annotated_image_url, stream=True).raw)
            st.subheader("Annotated Image")
            st.image(annotated_image, caption='Annotated Image', use_column_width=True)
    else:
        st.markdown('<p style="color: green; font-weight: bold;">No signs of diabetic retinal disease detected.</p>', unsafe_allow_html=True)
>>>>>>> 3155508fa94a1fc6ae13cfa3bfb25b05df3258e1
