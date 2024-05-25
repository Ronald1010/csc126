import streamlit as st
from PIL import Image, ImageDraw
from inference_sdk import InferenceHTTPClient
import tempfile

# Define the inference client details (replace with your actual API key and model ID)
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="VsxreoZsgrCDLK4xweXv"  # Replace with your Roboflow API key
)

MODEL_ID = "theeyedismodel.v2/1"  # Replace with your model ID

def classify_image(image):
    """Classifies an image using the Roboflow inference API.

    Args:
        image: A PIL Image object.

    Returns:
        A dictionary containing the classification results,
        or None if an error occurs.
    """

    try:
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image.save(temp_file, format="JPEG")
            temp_file_path = temp_file.name

        # Use the inference client to classify the image
        result = CLIENT.infer(temp_file_path, model_id=MODEL_ID)
        return result

    except Exception as e:
        print(f"Error during classification: {e}")
        return None

def draw_annotations(image, prediction):
    """Draws annotations on the image if bounding boxes are available.

    Args:
        image: A PIL Image object.
        prediction: A prediction from the model.

    Returns:
        An annotated PIL Image object.
    """
    draw = ImageDraw.Draw(image)
    if 'bbox' in prediction:
        box = prediction['bbox']
        class_name = prediction['class']
        draw.rectangle(
            [box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']],
            outline="red",
            width=3
        )
        draw.text((box['x'], box['y'] - 10), class_name, fill="red")
    return image

def generate_explanation(class_name):
    """Generates an explanation based on the class name.

    Args:
        class_name: The name of the classified class.

    Returns:
        A string containing an explanation of the class.
    """
    explanations = {
        "glaucoma": "The retina shows signs of glaucoma, a condition characterized by increased intraocular pressure leading to optic nerve damage.",
        "cataract": "The image indicates the presence of cataracts, where the lens becomes cloudy, leading to a decrease in vision.",
        "diabetic_retinopathy": "The image suggests diabetic retinopathy, a diabetes complication that affects the eyes by damaging the blood vessels of the retina.",
        "macular_degeneration": "Signs of macular degeneration are evident, which is a condition that results in the deterioration of the central portion of the retina, affecting central vision.",
        "healthy": "The retina appears healthy with no obvious signs of disease.",
        # Additional variations
        "Diabetic Retinopaty": "The image suggests diabetic retinopathy, a diabetes complication that affects the eyes by damaging the blood vessels of the retina."
    }
    return explanations.get(class_name, "No explanation available for this class.")

def main():
    """The main function of the script."""

    # Set page title and favicon
    st.set_page_config(page_title="Eye Disease Classification", page_icon="👁️")

    # Define app title and subtitle with emojis
    st.title("👁️ Eye Disease Classification")
    st.write(
        "Welcome to our Eye Disease Classification tool. Upload an image of the eye to get started!"
    )

    # Add space for better layout
    st.write("")

    # Add file uploader
    uploaded_file = st.file_uploader("Upload Eye Image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        st.subheader("Uploaded Eye Image")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Eye Image", use_column_width=True)

        # Classify the image
        with st.spinner("Classifying eye image..."):
            result = classify_image(image.copy())

        # Display results after preloader
        if result:
            # Extract and display the highest confidence prediction
            if "predictions" in result and result["predictions"]:
                predictions = result["predictions"]
                highest_confidence_prediction = max(predictions, key=lambda p: p["confidence"])
                
                st.subheader("Classification Result:")
                
                # Draw annotations on the image if bounding boxes are available
                annotated_image = draw_annotations(image.copy(), highest_confidence_prediction)
                st.image(annotated_image, caption="Annotated Eye Image", use_column_width=True)
                
                # Display the highest confidence prediction
                class_name = highest_confidence_prediction["class"]
                confidence = highest_confidence_prediction["confidence"]
                confidence_percentage = confidence * 100
                st.write(f"Detected Disease: {class_name}")
                st.write(f"Confidence: {confidence_percentage:.2f}%")
                
                # Generate and display explanation based on the result
                explanation = generate_explanation(class_name)
                st.subheader(f"Discussion of {class_name}:")
                st.write(explanation)
            else:
                st.write("No classification results found in the response.")
        else:
            st.markdown(
                '<p style="color: orange; font-weight: bold;">An error occurred during classification. Please check your API key, model ID, or image format.</p>',
                unsafe_allow_html=True,
            )

if __name__ == "__main__":
    main()
