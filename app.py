import streamlit as st
import pandas as pd
import random
import os
import plotly.express as px

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
        
        # Sort by Priority
        df = df.sort_values(by="Priority", ascending=False)
        
        # 1. CHARTS
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Complaints by Category")
            if not df.empty:
                fig1 = px.bar(df['Category'].value_counts(), title="Total per Category")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("📈 Status Overview")
            if not df.empty:
                fig2 = px.pie(df, names='Status', title="Status Breakdown")
                st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        st.subheader("📋 Manage Complaints")
        
        # 2. STATUS UPDATE
        for i in df.index:
            with st.expander(f"**Priority {df.loc[i, 'Priority']}** | {df.loc[i, 'Category']} - {df.loc[i, 'Description'][:50]}..."):
                st.write(f"**Full Description:** {df.loc[i, 'Description']}")
                
                new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Resolved"], 
                                          index=["Pending", "In Progress", "Resolved"].index(df.loc[i, 'Status']), key=f"status_{i}")
                
                new_comment = st.text_area("MP Comment", df.loc[i, 'Comment'], key=f"comment_{i}")
                
                if st.button("Save Update", key=f"save_{i}"):
                    df.loc[i, 'Status'] = new_status
                    df.loc[i, 'Comment'] = new_comment
                    df.to_csv(CSV_FILE, index=False)
                    st.success("Updated!")
                    st.rerun()

    elif user:
        st.error("Wrong credentials")