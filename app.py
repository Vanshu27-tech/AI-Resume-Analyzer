from flask import Flask, render_template, request, send_file
import os

# PDF Report
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Custom Modules
from utils.pdf_reader import extract_text
from models.skills_extractor import extract_skills
from models.ats_score import calculate_ats_score, missing_skills
from models.resume_parser import (
    extract_name,
    extract_email,
    extract_phone
)
from models.job_matcher import calculate_match
from models.resume_suggestions import generate_suggestions

app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store latest analysis
analysis_data = {}

# ===========================
# Home Page
# ===========================

@app.route("/")
def home():

    return render_template("index.html")


# ===========================
# Upload Resume + JD
# ===========================

@app.route("/upload", methods=["POST"])
def upload():

    global analysis_data

    # Check Resume

    if "resume" not in request.files:

        return "Resume not uploaded."

    # Check JD

    if "job_description" not in request.files:

        return "Job Description not uploaded."

    resume_file = request.files["resume"]

    jd_file = request.files["job_description"]

    # Resume Validation

    if resume_file.filename == "":

        return "Please choose Resume PDF."

    # JD Validation

    if jd_file.filename == "":

        return "Please choose Job Description PDF."

    # Save Resume

    resume_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume_file.filename
    )

    resume_file.save(resume_path)

    # Save JD

    jd_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        jd_file.filename
    )

    jd_file.save(jd_path)

    # Extract Resume Text

    resume_text = extract_text(resume_path)

    # Extract JD Text

    jd_text = extract_text(jd_path)

    if resume_text.strip() == "":

        return "Unable to extract Resume."

    if jd_text.strip() == "":

        return "Unable to extract Job Description."

    # Candidate Details

    name = extract_name(resume_text)

    email = extract_email(resume_text)

    phone = extract_phone(resume_text)

    # Resume Skills

    resume_skills = extract_skills(resume_text)

    # JD Skills

    jd_skills = extract_skills(jd_text)
        # ===========================
    # ATS Score
    # ===========================

    score = calculate_ats_score(
        resume_skills,
        jd_skills
    )

    # ===========================
    # Missing Skills
    # ===========================

    missing = missing_skills(
        resume_skills,
        jd_skills
    )

    # ===========================
    # Resume Match Percentage
    # ===========================

    match_score = calculate_match(
        resume_text,
        jd_text
    )

    # ===========================
    # AI Suggestions
    # ===========================

    suggestions = generate_suggestions(
        resume_text,
        resume_skills,
        jd_skills
    )

    # Suggestions based on JD

    for skill in missing:

        suggestions.append(
            f"Add '{skill}' to your resume because it appears in the Job Description."
        )

    # Remove duplicate suggestions

    suggestions = list(dict.fromkeys(suggestions))

    # ===========================
    # Save Analysis
    # ===========================

    analysis_data = {

        "name": name,

        "email": email,

        "phone": phone,

        "resume_text": resume_text,

        "jd_text": jd_text,

        "resume_skills": resume_skills,

        "jd_skills": jd_skills,

        "score": score,

        "match_score": match_score,

        "missing": missing,

        "suggestions": suggestions,

        "resume_file": resume_file.filename,

        "jd_file": jd_file.filename

    }

    # ===========================
    # Show Result Page
    # ===========================

    return render_template(

        "result.html",

        name=name,

        email=email,

        phone=phone,

        resume_text=resume_text,

        jd_text=jd_text,

        resume_file=resume_file.filename,

        jd_file=jd_file.filename,

        skills=resume_skills,

        jd_skills=jd_skills,

        score=score,

        match_score=match_score,

        missing=missing,

        suggestions=suggestions

    )
# ===========================
# Download PDF Report
# ===========================

@app.route("/download")
def download():

    pdf_file = "Resume_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = []

    # ===========================
    # Title
    # ===========================

    story.append(
        Paragraph(
            "AI Resume Analyzer Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # Candidate Information
    # ===========================

    story.append(
        Paragraph(
            f"<b>Name:</b> {analysis_data.get('name','')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Email:</b> {analysis_data.get('email','')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Phone:</b> {analysis_data.get('phone','')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # Uploaded Files
    # ===========================

    story.append(
        Paragraph(
            f"<b>Resume File:</b> {analysis_data.get('resume_file','')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Job Description File:</b> {analysis_data.get('jd_file','')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # Scores
    # ===========================

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {analysis_data.get('score',0)}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Resume Match:</b> {analysis_data.get('match_score',0)}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # Resume Skills
    # ===========================

    story.append(
        Paragraph(
            "<b>Skills Found</b>",
            styles["Heading2"]
        )
    )

    for skill in analysis_data.get("resume_skills", []):

        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # JD Skills
    # ===========================

    story.append(
        Paragraph(
            "<b>Job Description Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in analysis_data.get("jd_skills", []):

        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # Missing Skills
    # ===========================

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in analysis_data.get("missing", []):

        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    # ===========================
    # AI Suggestions
    # ===========================

    story.append(
        Paragraph(
            "<b>AI Suggestions</b>",
            styles["Heading2"]
        )
    )

    for suggestion in analysis_data.get("suggestions", []):

        story.append(
            Paragraph(
                f"• {suggestion}",
                styles["BodyText"]
            )
        )

    # Build PDF

    doc.build(story)

    return send_file(
        pdf_file,
        as_attachment=True
    )


# ===========================
# Run Flask App
# ===========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )