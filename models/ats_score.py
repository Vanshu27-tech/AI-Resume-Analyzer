"""
ATS Score Module

Calculates:
1. ATS Score (Resume Skills vs Job Description Skills)
2. Missing Skills
3. Matching Skills
"""


def calculate_ats_score(resume_skills, jd_skills):
    """
    Calculate ATS Score based on Resume Skills and JD Skills.

    Parameters:
        resume_skills (list): Skills extracted from Resume
        jd_skills (list): Skills extracted from Job Description

    Returns:
        int: ATS Score (0-100)
    """

    # If no skills found in JD
    if len(jd_skills) == 0:
        return 0

    resume_lower = [skill.lower() for skill in resume_skills]
    jd_lower = [skill.lower() for skill in jd_skills]

    matched = 0

    for skill in jd_lower:
        if skill in resume_lower:
            matched += 1

    score = (matched / len(jd_lower)) * 100

    return round(score)


def missing_skills(resume_skills, jd_skills):
    """
    Find skills present in JD but missing from Resume.
    """

    resume_lower = [skill.lower() for skill in resume_skills]

    missing = []

    for skill in jd_skills:
        if skill.lower() not in resume_lower:
            missing.append(skill)

    return missing


def matched_skills(resume_skills, jd_skills):
    """
    Return common skills between Resume and JD.
    """

    resume_lower = [skill.lower() for skill in resume_skills]

    matched = []

    for skill in jd_skills:
        if skill.lower() in resume_lower:
            matched.append(skill)

    return matched


def extra_skills(resume_skills, jd_skills):
    """
    Return skills present in Resume but not required in JD.
    """

    jd_lower = [skill.lower() for skill in jd_skills]

    extra = []

    for skill in resume_skills:
        if skill.lower() not in jd_lower:
            extra.append(skill)

    return extra