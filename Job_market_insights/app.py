import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re

st.title(" Job Market Insights: A Comprehensive Dashboard for Job Search, Skills Demand & Salary Analysis")
page = st.sidebar.radio("Home", ["Job Finder", "Job Outlook", "Salary Insights"])

if page == "Job Finder":
    @st.cache_data
    def load_data():
        return pd.read_csv("jlink.csv")  # Replace with your actual CSV file path

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
            st.write(" No jobs found. Try different selections.")
            
elif page == "Job Outlook":
    # Load the cleaned dataset
    @st.cache_data
    def load_data():
        df = pd.read_csv("egypt.csv")
        df.columns = df.columns.str.strip()  # Clean column names
        return df

    df = load_data()

    # Sidebar Navigation
    st.sidebar.title("skill")
    page = st.sidebar.radio("Go to:", ["📊 Market Overview", "🎯 Skills Analysis"  ])

    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_city = st.sidebar.selectbox("Select a City", ["All"] + sorted(df["Location"].dropna().unique()))
    df_filtered = df if selected_city == "All" else df[df["Location"] == selected_city]

    # Extract and count skills
    skill_series = df_filtered["Skills"].dropna().str.split(",").explode()


    if page == "📊 Market Overview":
        st.title("📊 Market Overview")

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

elif page == "Salary Insights":
    @st.cache_data
    def load_data():
        df = pd.read_csv("JOBS_Data_Cleaned.csv")
        return df

    df = load_data()


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
