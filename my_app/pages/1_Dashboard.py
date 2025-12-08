import streamlit as st
import pandas as pd
import numpy as np
from app.data.datasets_metadata import get_all_datasets_metadata, insert_datasets_metadata
from app.data.db import connect_database


st.set_page_config(page_title="Intelligence Dashboard",page_icon="📊", layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "role" not in st.session_state:
   st.session_role = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
  st.error("You must be logged in to view the dashboard.")
  if st.button("Go to login page"):
    st.switch_page("app.py") 
  st.stop()

# If logged in, show dashboard content
st.title(" Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")


# Sidebar filters
with st.sidebar:
  st.header("Filters")

  n_points = st.slider("Number of data points", 10, 200, 50)
  if st.button("Log out"):
     st.session_state.logged_in = False
     st.session_state.username = ""
     st.session_state.role = ""
     st.info("You have been logged out.")
     st.switch_page("app.py")

st.title("Datasets Dashboard")

name = st.text_input("Enter a name")
if st.button("Submit"):
    st.success(f"Hello {name}")

#Datasets metadatast.subheader("Datasets Metadata")
df_datasets = pd.read_csv("my_app/DATA/datasets_metadata.csv")
df_datasets.columns = df_datasets.columns.str.strip()

st.subheader("Datasets Metadata Table")
st.dataframe(df_datasets)

#Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("data_scientist", df_datasets[df_datasets["uploaded_by"] == "data_scientist"].shape[0])

with col2:
    st.metric("Datasets Metadata", df_datasets["uploaded_by"].count(), "1")


# Bar chart
uploaded_counts = df_datasets["uploaded_by"].value_counts()

if not uploaded_counts.empty:
 st.bar_chart(uploaded_counts)
else:
   st.warning("No dataset metadata available to plot.")

# Add Datasets
st.markdown("## Add Datasets ##")

with st.form("Add new Dataset"):
    dataset_id = st.text_input("Dataset ID")
    upload_date = st.date_input("Upload date")
    uploaded_by = st.text_input("Uploaded by", value=st.session_state.username) 
    name = st.selectbox("Dataset Name", ["customer_churn", "Financial_Fraud", "Server_Logs","Image_Classification", "HR_Salary"])
    rows = st.number_input("Number of rows", min_value=100, max_value=1000000, value=1000, step=100)
    columns = st.number_input("Number of columns", min_value=5, max_value=500, value=10, step=5)  
    
    submitted = st.form_submit_button("Add Dataset")  

    if submitted:
       new_row = {
          "dataset_id": dataset_id, 
          "name": name, 
          "rows": rows, 
          "columns": columns, 
          "uploaded_by": uploaded_by, 
          "upload_date": upload_date
        } 
       df_datasets = pd.concat(
          [df_datasets, pd.DataFrame([new_row])],
          ignore_index=True
       )
       df_datasets.to_csv("my_app/DATA/datasets_metadata.csv", index=False)

       st.success("Dataset added")
       st.rerun()


#data from datasets_metadata.csv
st.subheader("Dataset Visualizations")
numeric_cols = df_datasets.select_dtypes(include=["int64", "float64"]).columns.tolist()

if numeric_cols:
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Line chart")
    st.line_chart(df_datasets[numeric_cols])
  with col2:
    st.subheader("Bar chart")
    st.bar_chart(df_datasets[numeric_cols])
  with st.expander("See raw data"):
    st.dataframe(df_datasets[numeric_cols])
else:
   st.warning("No numeric columns found in the dataset.")

# Logout button
st.divider()
if st.button("Log out"):
  st.session_state.logged_in = False
  st.session_state.username = ""
  st.info("You have been logged out.")
  st.switch_page("app.py")

