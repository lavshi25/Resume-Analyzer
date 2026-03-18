import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python", "java", "javascript", "sql", "machine learning", "nlp",
    "flask", "django", "react", "html", "css", "tensorflow", "pandas",
    "numpy", "git", "docker", "aws", "communication", "teamwork",
    "data analysis", "deep learning", "keras", "scikit-learn", "mongodb",
    "rest api", "node.js", "c++", "linux", "excel", "power bi", "tableau"
]

def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILL_KEYWORDS if skill in text_lower]

def get_match_score(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def get_missing_skills(resume_skills, job_description):
    job_desc_lower = job_description.lower()
    required = [skill for skill in SKILL_KEYWORDS if skill in job_desc_lower]
    return [s for s in required if s not in resume_skills]

def get_suggestions(missing_skills, score):
    suggestions = []
    if missing_skills:
        suggestions.append(f"Add these missing skills to your resume: {', '.join(missing_skills)}")
    if score < 40:
        suggestions.append("Your resume needs significant tailoring for this role.")
    elif score < 70:
        suggestions.append("Good start! Customize your summary section to mirror the job description.")
    else:
        suggestions.append("Strong match! Make sure your experience section uses similar keywords.")
    suggestions.append("Use strong action verbs: built, designed, improved, led, optimized.")
    suggestions.append("Quantify achievements where possible (e.g. 'improved performance by 30%').")
    suggestions.append("Keep your resume to 1 page if you have under 5 years of experience.")
    return suggestions