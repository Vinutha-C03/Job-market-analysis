import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.title("Job Market Insights Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("JOBS_Data_Cleaned.csv")
    return df

df = load_data()

# # Sidebar Filters
# st.sidebar.header("Filter Options")
# job_filter = st.sidebar.selectbox("Select Job Title", ["All"] + list(df["Job Title"].unique()))
# location_filter = st.sidebar.selectbox("Select Location", ["All"] + list(df["Location"].unique()))

# Apply filters
# filtered_df = df.copy()
# if job_filter != "All":
#     filtered_df = filtered_df[filtered_df["Job Title"] == job_filter]
# if location_filter != "All":
#     filtered_df = filtered_df[filtered_df["Location"] == location_filter]

# Function to extract salary
def extract_salary(salary_str):
    salary_str = re.sub(r'[^\d\-]', '', str(salary_str))
    salary_numbers = re.findall(r'\d+', salary_str)
    
    if len(salary_numbers) >= 2:
        return (int(salary_numbers[0]) + int(salary_numbers[1])) / 2
    elif len(salary_numbers) == 1:
        return int(salary_numbers[0])
    return None

# Process Salary Data
df["Avg Salary"] = df["Salary Estimate"].apply(extract_salary)
df.dropna(subset=["Avg Salary"], inplace=True)

# 🔹 Job Openings by Industry
st.subheader("Job Openings by Industry")
if "Industry" in df.columns:
    industry_counts = df["Industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Count"]
    
    fig = px.bar(industry_counts, x="Count", y="Industry", orientation="h",
                 title="Job Openings by Industry", color="Count", color_continuous_scale="blues")
    st.plotly_chart(fig)
else:
    st.write("Industry data is not available in this dataset.")

# 🔹 Salary Distribution
st.subheader("Salary Distribution")
selected_job_title = st.selectbox("Select Job Title for Salary Distribution", ["All"] + list(df["Job Title"].unique()))

df_salary_filtered = df if selected_job_title == "All" else df[df["Job Title"] == selected_job_title]

fig = px.histogram(df_salary_filtered, x="Avg Salary", nbins=30, 
                   title=f"Salary Distribution for {selected_job_title}",
                   color_discrete_sequence=["#636EFA"], marginal="box")
st.plotly_chart(fig)

# 🔹 Salary Comparison by Location
st.subheader("Salary Comparison by Location")
selected_job_title_loc = st.selectbox("Select Job Title for Salary Comparison", ["All"] + list(df["Job Title"].unique()))

df_loc_filtered = df if selected_job_title_loc == "All" else df[df["Job Title"] == selected_job_title_loc]

fig = px.violin(df_loc_filtered, x="Location", y="Avg Salary", box=True, points="all",
                title=f"Salary Comparison by Location for {selected_job_title_loc}",
                color="Location")
st.plotly_chart(fig)

# 🔹 Skills Demand Analysis
st.subheader("Skills Demand Analysis by Job Title")
selected_job_title_skill = st.selectbox("Select Job Title for Skill Analysis", ["All"] + list(df["Job Title"].unique()))

df_skill_filtered = df if selected_job_title_skill == "All" else df[df["Job Title"] == selected_job_title_skill]

skills = ["Python", "SQL", "Machine Learning", "Deep Learning", "Tableau", "Power BI", 
          "NLP", "Big Data", "Hadoop", "Spark", "AWS"]

skill_counts = {skill: df_skill_filtered["Job Description"].str.contains(skill, case=False, na=False).sum() 
                for skill in skills}

skill_df = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Count"])

fig = px.bar(skill_df, x="Skill", y="Count", title=f"Skills Demand Analysis for {selected_job_title_skill}",
             color="Count", color_continuous_scale="viridis")
st.plotly_chart(fig)
