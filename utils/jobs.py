JOB_DATABASE = [
    {"title": "Python Developer", "skills": ["python", "flask", "sql", "git"]},
    {"title": "Data Analyst", "skills": ["python", "pandas", "sql", "excel", "tableau"]},
    {"title": "ML Engineer", "skills": ["machine learning", "python", "tensorflow", "deep learning", "keras"]},
    {"title": "Frontend Developer", "skills": ["html", "css", "javascript", "react"]},
    {"title": "Backend Developer", "skills": ["python", "django", "sql", "docker", "rest api"]},
    {"title": "Data Scientist", "skills": ["python", "pandas", "numpy", "machine learning", "sql"]},
    {"title": "DevOps Engineer", "skills": ["docker", "linux", "aws", "git"]},
    {"title": "Full Stack Developer", "skills": ["html", "css", "javascript", "python", "sql", "git"]},
]

def recommend_jobs(resume_skills):
    results = []
    for job in JOB_DATABASE:
        matched = [s for s in job["skills"] if s in resume_skills]
        score = round(len(matched) / len(job["skills"]) * 100)
        results.append({
            "title": job["title"],
            "match": score,
            "matched_skills": matched
        })
    return sorted(results, key=lambda x: x["match"], reverse=True)[:5]