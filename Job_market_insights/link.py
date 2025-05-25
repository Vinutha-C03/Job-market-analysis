import streamlit as st
import pandas as pd

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("jlink.csv")  

df = load_data()

# Streamlit UI
st.title("🔍 Job Finder")
st.write("Select job title and location to find relevant job listings.")

# Dropdown for Job Title & Location
job_title_options = ["All"] + sorted(df["Job Title"].dropna().unique())
location_options = ["All"] + sorted(df["Location"].dropna().unique())

job_title = st.selectbox("Select Job Title", job_title_options)
location = st.selectbox("Select Location", location_options)

# Filter results when the user clicks Search
if st.button("Search"):
    filtered_df = df.copy()

    if job_title != "All":
        filtered_df = filtered_df[filtered_df["Job Title"].str.contains(job_title, case=False, na=False)]
    
    if location != "All":
        filtered_df = filtered_df[filtered_df["Location"].str.contains(location, case=False, na=False)]
    
    if not filtered_df.empty:
        st.dataframe(filtered_df[['Job Title', 'Company', 'Location', 'Job Link']])
    else:
        st.write("❌ No jobs found. Try different selections.")
