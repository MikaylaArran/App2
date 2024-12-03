{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
\
# App title and description\
st.title("Automated Reconciliation System")\
st.write("This app extracts text from uploaded images of slips and bank statements, then reconciles the data.")\
\
# File upload fields\
slip_image = st.file_uploader("Upload Slip Image", type=["jpg", "png", "jpeg"])\
bank_image = st.file_uploader("Upload Bank Statement Image", type=["jpg", "png", "jpeg"])\
\
if slip_image and bank_image:\
    st.write("Files uploaded successfully! Proceeding to process images...")\
from PIL import Image\
import pytesseract\
\
if slip_image and bank_image:\
    # Load images\
    slip_img = Image.open(slip_image)\
    bank_img = Image.open(bank_image)\
\
    # Extract text using OCR\
    slip_text = pytesseract.image_to_string(slip_img)\
    bank_text = pytesseract.image_to_string(bank_img)\
\
    # Display extracted text\
    st.subheader("Extracted Text from Slip")\
    st.text(slip_text)\
\
    st.subheader("Extracted Text from Bank Statement")\
    st.text(bank_text)\
import pandas as pd\
\
if slip_image and bank_image:\
    # Convert text to lists\
    slips = [line.strip() for line in slip_text.splitlines() if line.strip()]\
    bank_statements = [line.strip() for line in bank_text.splitlines() if line.strip()]\
\
    # Perform reconciliation\
    recon_results = []\
    for slip in slips:\
        if slip in bank_statements:\
            recon_results.append(\{"Slip Entry": slip, "Status": "Match Found"\})\
        else:\
            recon_results.append(\{"Slip Entry": slip, "Status": "No Match"\})\
\
    # Display results as a table\
    df = pd.DataFrame(recon_results)\
    st.subheader("Reconciliation Results")\
    st.dataframe(df)\
@st.cache\
def convert_df_to_csv(df):\
    return df.to_csv(index=False).encode('utf-8')\
\
if slip_image and bank_image and not df.empty:\
    csv = convert_df_to_csv(df)\
    st.download_button(\
        label="Download Reconciliation Report",\
        data=csv,\
        file_name='reconciliation_report.csv',\
        mime='text/csv',\
    )\
}