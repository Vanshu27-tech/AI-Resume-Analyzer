def generate_suggestions(resume_text, resume_skills, jd_skills=None):
    """
    Generate AI-based suggestions to improve the resume.

    Parameters:
        resume_text (str): Extracted resume text
        resume_skills (list): Skills found in resume
        jd_skills (list): Skills found in Job Description (optional)

    Returns:
        list: Suggestions
    """

    suggestions = []

    text = resume_text.lower()

    # ==========================
    # Resume Sections
    # ==========================

    if "project" not in text:
        suggestions.append(
            "Add a Projects section with detailed project descriptions."
        )

    if "certification" not in text:
        suggestions.append(
            "Include your Certifications section."
        )

    if "internship" not in text:
        suggestions.append(
            "Mention internships or practical work experience."
        )

    if "achievement" not in text:
        suggestions.append(
            "Add achievements or awards to strengthen your profile."
        )

    if "github" not in text:
        suggestions.append(
            "Include your GitHub profile link."
        )

    if "linkedin" not in text:
        suggestions.append(
            "Include your LinkedIn profile link."
        )

    # ==========================
    # Important Skills
    # ==========================

    important_skills = [
        "Python",
        "SQL",
        "Git",
        "GitHub",
        "Flask",
        "React",
        "Docker",
        "Machine Learning",
        "JavaScript",
        "HTML",
        "CSS"
    ]

    for skill in important_skills:

        if skill not in resume_skills:

            suggestions.append(
                f"Consider learning and adding '{skill}' to your resume."
            )

    # ==========================
    # JD Based Suggestions
    # ==========================

    if jd_skills:

        resume_lower = [skill.lower() for skill in resume_skills]

        for skill in jd_skills:

            if skill.lower() not in resume_lower:

                suggestions.append(
                    f"The Job Description requires '{skill}'. Add this skill if you have experience with it."
                )

    # ==========================
    # ATS Tips
    # ==========================

    suggestions.append(
        "Use action verbs like Developed, Built, Designed, and Implemented."
    )

    suggestions.append(
        "Keep your resume limited to one or two pages."
    )

    suggestions.append(
        "Quantify your achievements wherever possible."
    )

    suggestions.append(
        "Tailor your resume according to the Job Description."
    )

    # ==========================
    # Remove Duplicate Suggestions
    # ==========================

    suggestions = list(dict.fromkeys(suggestions))

    return suggestions