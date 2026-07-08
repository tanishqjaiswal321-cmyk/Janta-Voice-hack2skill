import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Janata Voice", layout="wide")
st.title("🇮🇳 Janata Voice - People's Priorities")

CSV_FILE = "complaints.csv"
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Category", "Description", "Priority", "Status", "Comment"])

menu = st.sidebar.selectbox("Login as", ["Citizen", "MP Office"])

if menu == "Citizen":
    st.header("📝 Submit Your Issue")
    category = st.selectbox("Category", ["Road", "Water", "Electricity", "Garbage", "Other"])
    desc = st.text_area("Describe the problem")
    
    if st.button("Submit Complaint"):
        if desc.strip() == "":
            st.error("Please describe the problem")
        else:
            priority = random.randint(70, 99)
            new_row = {"Category": category, "Description": desc, "Priority": priority, "Status": "Pending", "Comment": ""}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success(f"✅ Submitted! Priority: {priority}")

elif menu == "MP Office":
    st.header("🏢 MP Office Dashboard")
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    if user == "mpadmin" and passw == "1234":
        st.success("Logged in")
        st.dataframe(df)
    elif user:
        st.error("Wrong credentials")
