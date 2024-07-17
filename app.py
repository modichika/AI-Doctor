import streamlit as st 
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

genai.configure(api_key = api_key)


generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

system_prompt = """


As a highly skilled medical practitioner specializing in image analysis ,you are tasked with examining medical images for a renowned hospital . Your expertise is crucial in identifying any anomalies  , diseases , or health issues that may be present in the images . 

Your responsibilities include :

1. Symptoms : What are the symptoms for the disease
2. Detailed Analysis : Thoroughly analyze each image , focusing on identifying any abnormal findings.
3. Findings Report : Document all observred anomalies or signs of disease . Clearly articulate these findings in structured format .
4. Recommendation and Next Steps : Based on your analysis , suggest potential next steps , including further tests or treatments as applicable
5. Treatment Suggestions: If appropriate , recommend possible  treatement options or interventions , 


Important Notes:

1. Scope of Response : Only respond if the image pertains to human health issues . 
2.Clarity of Image: In cases where the image quality impedes clear analysis , note that certain aspects are 'Unable to determine based on provided image'.
3.Disclaimer : Accompany your analysis with disclaimer "Consult with your nearby doctor before making any decisions this is just an LLm model".
4. Your insights are invaluable in guiding clinical decisions . please proceed with anaylsis , adhering to structured approach outlined above


Please Provide me an output with these five headings 



"""

safety_setting = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
     {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
     {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
     {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  safety_settings = safety_setting
)

st.set_page_config(page_title = 'medical app' , page_icon = ':robot:')

st.image("https://t4.ftcdn.net/jpg/02/60/04/09/360_F_260040900_oO6YW1sHTnKxby4GcjCvtypUCWjnQRg5.jpg" , width = 200 )

st.title("⚕️Medical Image analytics🩺")

st.subheader("I am Dr Maity , you can submit your image here and I will give detailed analysis of your medical image")

upload_file = st.file_uploader("Upload an image",type=["png","jpg","jpeg"])
if upload_file:
    st.image(upload_file,width = 300,caption = "Uploaded Image")

submit_button = st.button("Generate the diagnosis")

if submit_button:
    image_data = upload_file.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        }, 
    ]

    prompt_parts = [
        image_parts[0],
        system_prompt
    ]

    

    response = model.generate_content(prompt_parts)

    st.title("Here is the analysis which Dr.Maity gave")
    st.write(response.text)