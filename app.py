from flask import Flask, request, jsonify, render_template
import os

from utils.parser import extract_text
from utils.nlp_engine import extract_skills, get_match_score, get_missing_skills, get_suggestions
from utils.jobs import recommend_jobs

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")
    job_desc = request.form.get("job_description", "")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    if not job_desc.strip():
        return jsonify({"error": "No job description provided"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    resume_text = extract_text(path)
    skills = extract_skills(resume_text)
    score = get_match_score(resume_text, job_desc)
    missing = get_missing_skills(skills, job_desc)
    suggestions = get_suggestions(missing, score)
    jobs = recommend_jobs(skills)

    return jsonify({
        "score": score,
        "skills_found": skills,
        "missing_skills": missing,
        "suggestions": suggestions,
        "job_recommendations": jobs
    })

if __name__ == "__main__":
    app.run(debug=True)