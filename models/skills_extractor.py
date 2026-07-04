skills = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Flask",
    "Django",
    "Machine Learning",
    "React",
    "Node.js",
    "Git",
    "GitHub",
    "MongoDB",
    "MySQL"
]

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills