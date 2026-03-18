function updateFileLabel(input) {
  const label = document.getElementById("fileLabel");
  label.textContent = input.files[0] ? input.files[0].name : "Click to upload PDF or DOCX";
}

async function analyze() {
  const file = document.getElementById("resumeFile").files[0];
  const jobDesc = document.getElementById("jobDesc").value.trim();

  if (!file) return alert("Please upload your resume.");
  if (!jobDesc) return alert("Please paste a job description.");

  const btn = document.getElementById("analyzeBtn");
  const btnText = document.getElementById("btnText");
  const spinner = document.getElementById("spinner");

  btn.disabled = true;
  btnText.textContent = "Analyzing...";
  spinner.classList.remove("hidden");

  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDesc);

  try {
    const res = await fetch("/analyze", { method: "POST", body: formData });
    const data = await res.json();

    if (data.error) {
      alert("Error: " + data.error);
      return;
    }

    showResults(data);
  } catch (err) {
    alert("Something went wrong. Make sure Flask is running.");
  } finally {
    btn.disabled = false;
    btnText.textContent = "Analyze Resume";
    spinner.classList.add("hidden");
  }
}

function showResults(data) {
  document.getElementById("results").classList.remove("hidden");

  // Animate score ring
  const score = data.score;
  const circle = document.getElementById("scoreCircle");
  const circumference = 314;
  const offset = circumference - (score / 100) * circumference;
  circle.style.transition = "stroke-dashoffset 1s ease";
  circle.style.strokeDashoffset = offset;

  document.getElementById("scoreVal").textContent = score;

  const label = document.getElementById("scoreLabel");
  if (score >= 70) label.textContent = "Excellent Match!";
  else if (score >= 40) label.textContent = "Moderate Match — Room to Improve";
  else label.textContent = "Low Match — Needs Tailoring";

  // Skills
  document.getElementById("skillsFound").innerHTML =
    data.skills_found.length
      ? data.skills_found.map(s => `<span>${s}</span>`).join("")
      : `<span style="background:#f1f5f9;color:#94a3b8">None detected</span>`;

  document.getElementById("missingSkills").innerHTML =
    data.missing_skills.length
      ? data.missing_skills.map(s => `<span>${s}</span>`).join("")
      : `<span style="background:#f0fdf4;color:#16a34a">No gaps found!</span>`;

  // Suggestions
  document.getElementById("suggestions").innerHTML =
    data.suggestions.map(s => `<li>${s}</li>`).join("");

  // Job recommendations
  document.getElementById("jobRecs").innerHTML =
    data.job_recommendations.map(j => `
      <div class="job-card">
        <div>
          <div class="job-title">${j.title}</div>
          <div class="job-skills">${j.matched_skills.join(", ") || "No direct skill matches"}</div>
        </div>
        <div class="job-match">${j.match}%</div>
      </div>
    `).join("");

  document.getElementById("results").scrollIntoView({ behavior: "smooth" });
}