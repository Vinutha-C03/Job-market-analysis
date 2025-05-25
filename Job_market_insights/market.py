import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import folium
from streamlit_folium import folium_static
import plotly.express as px

# Load the cleaned dataset
@st.cache_data
def load_data():
    df = pd.read_csv("egypt.csv")
    df.columns = df.columns.str.strip()  # Clean column names
    return df

df = load_data()

# Sidebar Navigation
st.sidebar.title("📂 Dashboard Navigation")
page = st.sidebar.radio("Go to:", ["📊 Job Market Overview", "🎯 Skills Analysis"  ])

# Sidebar Filters
st.sidebar.header("Filters")
selected_city = st.sidebar.selectbox("Select a City", ["All"] + sorted(df["Location"].dropna().unique()))
df_filtered = df if selected_city == "All" else df[df["Location"] == selected_city]

# Extract and count skills
skill_series = df_filtered["Skills"].dropna().str.split(",").explode()


#  JOB MARKET OVERVIEW PAGE

if page == "📊 Job Market Overview":
    st.title("📊 Job Market Overview")

    # 🔹 Top Job Titles Demand
    st.subheader("💼 Job Title Demand")
    job_counts = df_filtered["Job title"].value_counts().head(10)
    fig, ax = plt.subplots()
    job_counts.sort_values().plot(kind="barh", color="skyblue", ax=ax)
    ax.set_xlabel("Job Count")
    ax.set_ylabel("Job Title")
    ax.set_title("Top 10 Job Titles by Demand")
    st.pyplot(fig)

    # 🔹 Top Hiring Companies
    st.subheader("🏢 Top Hiring Companies")
    company_counts = df_filtered["Company name"].value_counts().head(10)
    fig, ax = plt.subplots()
    company_counts.sort_values().plot(kind="barh", color="orange", ax=ax)
    ax.set_xlabel("Job Count")
    ax.set_ylabel("Company Name")
    ax.set_title("Top 10 Companies Hiring")
    st.pyplot(fig)


#  SKILLS ANALYSIS PAGE

elif page == "🎯 Skills Analysis":
    st.title("🎯 Skills Analysis")

  
# 🔹 Skills Demand (Bubble Chart)
    st.subheader("🟢 Skills Demand (Bubble Chart)")

# Count occurrences of each skill
    top_skills = skill_series.value_counts().head(10).reset_index()
    top_skills.columns = ["Skill", "Count"]

# Create a bubble chart
    fig = px.scatter(
        top_skills, 
        x="Skill", 
        y="Count", 
        size="Count", 
        color="Skill",
        title="Top 10 In-Demand Skills",
        size_max=60
    )

    st.plotly_chart(fig)


    # 🔹 Job Title vs. Skills Count
    st.subheader("🔥 Job Title vs. Skills Count")
    skill_counts_per_job = df_filtered.groupby("Job title")["Skills"].count().reset_index()
    skill_counts_per_job = skill_counts_per_job.sort_values(by="Skills", ascending=False).head(10)

    fig, ax = plt.subplots()
    sns.barplot(x="Skills", y="Job title", data=skill_counts_per_job, palette="Blues", ax=ax)
    ax.set_xlabel("Skills Count")
    ax.set_ylabel("Job Title")
    st.pyplot(fig)

    # 🔹 Top 10 In-Demand Skills (Pie Chart)
    st.subheader("🎯 Top 10 In-Demand Skills")
    top_skills = skill_series.value_counts().head(10)
    fig, ax = plt.subplots()
    ax.pie(top_skills, labels=top_skills.index, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
    ax.axis("equal")  # Equal aspect ratio ensures pie is drawn as a circle.
    st.pyplot(fig)

