import pandas as pd
import ast
from collections import Counter
import matplotlib.pyplot as plt

# Data Understanding

df= pd.read_csv("gsearch_jobs.csv")
print(df.head())
print(df.shape)
print(df.info())
print(df.columns.tolist())
print(df["description_tokens"].head())
print(df["title"].value_counts().head(20))

#job titles

print("\n===== TOP 20 JOB TITLES =====")

print(df["title"].value_counts().head(20))

df["title"] = df["title"].str.lower().str.strip()

#skills

all_skills = []

for skills in df["description_tokens"]:

    try:
        skill_list = ast.literal_eval(skills)
        all_skills.extend(skill_list)

    except Exception:
        pass
skill_series = pd.Series(all_skills)

print("\n===== TOP 20 SKILLS =====")

print(skill_series.value_counts().head(20))

#Salary 

print("\n===== SALARY OVERVIEW =====")

print(df["salary_standardized"].describe())

print("\n===== TOP 20 COMPANIES =====")
print(df["company_name"].value_counts().head(20))

top_skills = skill_series.value_counts().head(10)

plt.figure(figsize=(10,5))

top_skills.plot(kind="bar")

plt.title("Top 10 In-Demand Skills")

plt.xlabel("Skills")

plt.ylabel("Job Count")

plt.tight_layout()


plt.figure(figsize=(10,5))

df["salary_standardized"].dropna().hist(bins=30)

plt.title("Salary Distribution")

plt.xlabel("Salary")

plt.ylabel("Number of Jobs")

plt.show()

#Remote work
print("\n===== REMOTE WORK ANALYSIS =====")

print(df["work_from_home"].value_counts(dropna=False))

print("\n===== JOB TYPE ANALYSIS =====")

print(df["schedule_type"].value_counts().head(10))

project_df = df[[
    "title",
    "company_name",
    "location",
    "work_from_home",
    "schedule_type",
    "salary_standardized"
]]

project_df.to_csv(
    "powerbi_dataset.csv",
    index=False
)

print("Dataset exported successfully!")

df["title"] = df["title"].str.lower().str.strip()

df["company_name"] = df["company_name"].str.strip()

df["location"] = df["location"].fillna("Unknown")

total_jobs = len(df)

avg_salary = df["salary_standardized"].mean()

top_company = df["company_name"].value_counts().idxmax()

top_role = df["title"].value_counts().idxmax()

print("\n===== KPI SUMMARY =====")

print("Total Jobs:", total_jobs)

print("Average Salary:", round(avg_salary, 2))

print("Top Company:", top_company)

print("Top Role:", top_role)

print("\n===== TOP 10 COMPANIES =====")

print(df["company_name"].value_counts().head(10))

#skills.csv

skills_df = df[["description_tokens"]]

skills_df.to_csv(
    "skills_dataset.csv",
    index=False
)

print("Skills dataset exported!")

all_skills = []

for skills in df["description_tokens"]:
    try:
        skill_list = ast.literal_eval(skills)
        all_skills.extend(skill_list)
    except Exception:
        pass

skill_counts = Counter(all_skills)

skills_summary = pd.DataFrame(
    skill_counts.items(),
    columns=["Skill", "Demand"]
)

skills_summary = skills_summary.sort_values(
    by="Demand",
    ascending=False
)

print(skills_summary.head(20))

skills_summary.to_csv(
    "skills_summary.csv",
    index=False
)

print("skills_summary.csv created successfully!")