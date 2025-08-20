import pandas as pd
from resume_optimizer import process_resume, get_embedding, cosine_similarity
from openai import OpenAI

# Load scraped jobs
jobs_df = pd.read_csv("jobs.csv")

# Load your resume text (use your existing function from resume-optimizer)
resume_text = process_resume("Monit Resume.pdf")

# Get embedding for resume
resume_embedding = get_embedding(resume_text)

# Rank jobs
ranked_jobs = []
for _, row in jobs_df.iterrows():
    job_text = f"{row['title']} at {row['company']}"
    job_embedding = get_embedding(job_text)
    score = cosine_similarity(resume_embedding, job_embedding)
    ranked_jobs.append((row['title'], row['company'], row['link'], score))

# Sort by similarity
ranked_jobs = sorted(ranked_jobs, key=lambda x: x[3], reverse=True)

# Show top 5
print("\nTop 5 matching jobs for you:\n")
for job in ranked_jobs[:5]:
    print(f"{job[0]} at {job[1]} → {job[2]} (score: {job[3]:.2f})")
