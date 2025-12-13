import streamlit as st
import pandas as pd
import numpy as np
from models.dataset import DatasetMetadata
from services.database_manager import DatabaseManager

db = DatabaseManager("database/intelligence_plaform.db")
db.connect()

st.set_page_config(page_title="Intelligence Dashboard",page_icon="📊", layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "role" not in st.session_state:
   st.session_state.role = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
  st.error("You must be logged in to view the dashboard.")
  if st.button("Go to login page"):
    st.switch_page("Login.py") 
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
     st.switch_page("Login.py")

st.title("Datasets Dashboard")

name = st.text_input("Enter a name")
if st.button("Submit"):
    st.success(f"Hello {name}")

rows = db.fetch_all(
    "SELECT dataset_id, dataset_name, file_size_mb, record_count, last_updated, source, created_at FROM datasets_metadata")
datasets: list[DatasetMetadata] = []
for row in rows:
    dataset = DatasetMetadata(
        dataset_id=row[0],
        dataset_name=row[1],
        file_size_mb=row[2],
        record_count=row[3],
        source=row[4],
        last_updated=row[5],
        created_at=row[6]

    )
    datasets.append(dataset)
df_datasets_db = pd.DataFrame([{
    "ID": d.get_id(),
    "Name": d.get_name(),
    "Size (MB)": round(d.get_size_mb(), 2),
    "Source": d.get_source()
} for d in datasets])

if not df_datasets_db.empty:
    st.dataframe(df_datasets_db)
else:
    st.warning("No datasets found in the database.")


#data from datasets_metadata.csv
st.subheader("Dataset Visualizations")
numeric_cols = df_datasets_db.select_dtypes(include=["int64", "float64"]).columns.tolist()

if numeric_cols:
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Line chart")
    st.line_chart(df_datasets_db[numeric_cols])
  with col2:
    st.subheader("Bar chart")
    st.bar_chart(df_datasets_db[numeric_cols])
  with st.expander("See raw data"):
    st.dataframe(df_datasets_db[numeric_cols])
else:
   st.warning("No numeric columns found in the dataset.")

# Logout button
st.divider()
if st.button("Log out"):
  st.session_state.logged_in = False
  st.session_state.username = ""
  st.info("You have been logged out.")
  st.switch_page("Login.py")