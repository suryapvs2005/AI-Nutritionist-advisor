# Install required libraries first:
# pip install python-dotenv streamlit google-generativeai pillow

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
model = genai.GenerativeModel('gemini-pro-vision')

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_prompt, image, user_input):
    response = model.generate_content([input_prompt, image[0], user_input])
    return response.text

# Function to handle uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="AI Nutritionist")
st.header("AI Nutritionist App")

user_input = st.text_area("Input your question (optional):", key="input")

uploaded_file = st.file_uploader("Upload a food image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Define the prompts
calorie_prompt = """
You are an expert nutritionist. Analyze the food items in the image and calculate the total calories.
Provide details of every food item and calorie intake like:

1. Item 1 - no of calories
2. Item 2 - no of calories
---
---
"""

diet_prompt = """
You are an expert nutritionist. Analyze the food items in the image and suggest a best balanced diet.
Provide details like:

1. Item 1 - no of calories
2. Item 2 - no of calories
3. Item 3 - no of calories
---
---
"""

inspection_prompt = """
You are an expert food inspector. Analyze the uploaded image and determine:
- Is it a food item?
- Is it safe for health?
- Why is it healthy or unhealthy?
"""

# Buttons
if st.button("Tell me the total calories"):
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(calorie_prompt, image_data, user_input)
        st.subheader("Result:")
        st.write(response)
    else:
        st.error("Please upload an image first.")

if st.button("Suggest a healthy diet"):
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(diet_prompt, image_data, user_input)
        st.subheader("Result:")
        st.write(response)
    else:
        st.error("Please upload an image first.")

if st.button("Food Inspector Report"):
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(inspection_prompt, image_data, user_input)
        st.subheader("Result:")
        st.write(response)
    else:
        st.error("Please upload an image first.")
