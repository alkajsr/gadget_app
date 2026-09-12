import streamlit as st
from google import genai
from google.genai import errors
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
     API_KEY = st.secrets["API_KEY"]

if not API_KEY:
     st.error("API Key missing")

client = genai.Client(api_key = API_KEY)

st.title("AI Electronic Gadgets Suggestor Recommender")
     
st.markdown("""
    <style>
    .stApp {
    background:linear-gradient(to right,#B5E48C,#FFFFFF)}
     </style>
     """,unsafe_allow_html=True)

placeholder = st.empty()

with placeholder.container(border= True):
    prompt=""
    sub_prompt=False
    submitted = False
    
    user = st.text_input("Your name")
    gadget_type = st.selectbox("Select Category",["Select an option","Laptops","Mobile Phones",
                "Earphones"])
    no = st.slider("Top:",1,10)

    if gadget_type == "Laptops":
        brand = st.multiselect("Brands",["HP","Dell","Lenovo","Acer","Samsung","Any"])
        purpose = st.multiselect("Purpose",["Browsing Internet","Programming","Working","Gaming","Editing","All purpose"])
        price_range = st.selectbox("Price range",["Upto 50,000","50,000 to 1,00,000","Over 1,00,000"])
        flag =1
        if brand and purpose and price_range:
            sub_prompt= f"""{gadget_type} of particular brand/brands of given user's choice - {",".join(brand)} brand, 
                           for {",".join(purpose)} purpose and of price {price_range} rupees in India"""
        
    elif gadget_type == "Mobile Phones":
        brand = st.multiselect("Select brand",["Samsung","Redmi","Motorola","Oneplus","Apple","Any"])
        price_range = st.selectbox("Price range",["<10,000","10,000-20,000","20,000-40,000",">40,000"])
        storage = st.selectbox("Storage Capacity",["4 GB","16 GB","32 GB","64 GB","128 GB",">128GB"])
        flag =2
        if brand and price_range and storage:
            sub_prompt= f"""{gadget_type} of particular brand/brands of given user's choice - {",".join(brand)} brand, 
                             storage capacity of {storage} and of price {price_range} rupees in India"""

    elif gadget_type == "Earphones":
        type = st.multiselect("Type",["Wired Earphones","Bluetooth Earphones","Wired Headphones","Bluetooth Headphones"])
        purpose = st.multiselect("Purpose",["Noise Cancelling","Bass","Sports","Gaming"])
        flag =3
        if type and purpose:
            sub_prompt= f"""{gadget_type} of particular brand/brands of given user's choice - {",".join(type)} type, 
                              for {",".join(purpose)} purpose in India"""
    else:
         sub_prompt = False
    if sub_prompt:
         submitted = st.button("**Generate Recommendations**",type="primary")
    else:
        st.error("Please provide all the details.")

      
if submitted:
    placeholder.empty()
    if  user and gadget_type and no and sub_prompt:
       prompt = f"""Suggest user named {user} top {no} {sub_prompt} with high rating and good customer review. Also suggest and compare
                online platforms where the user can buy it based on affordability, discount available and better customer reviews.
                Please keep the words simple, friendly and engaging in less than 200 words."""
       st.write("Analyzing and suggesting you recommendations with AI......")
       try:
           response = client.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents = prompt
            )
           st.write(response.text)
       except errors.APIError as e:
           st.write(f"API Error occurred [Status {e.code}]: {e.message}")   
       except Exception as e:
           st.write(f"An unexcepted error occurred: {e}")

    if st.button("Clear"):
         st.session_state.response = ""
         st.rerun()

