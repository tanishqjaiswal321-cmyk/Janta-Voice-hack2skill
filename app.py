import streamlit as st
import pandas as pd

st.set_page_config(page_title="Janata Voice", page_icon="🗣️")
st.title("🗣️ Janata Voice - People's Priorities")
st.subheader("AI-powered feedback for MP Office")

option = st.selectbox("Submit your issue", ["Road", "Water", "Electricity", "School", "Health"])
desc = st.text_area("Describe your problem in Hindi/English")
uploaded_file = st.file_uploader("Upload Photo")

if st.button("Submit"):
    st.success("Complaint submitted! AI will analyze and add to dashboard")
    st.info(f"Category: {option} | Priority Score: 87/100")

st.divider()
st.map(pd.DataFrame({'lat':[28.6], 'lon':[77.2]}))
st.caption("Heatmap of complaints in your constituency")
