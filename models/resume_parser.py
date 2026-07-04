import re


def extract_name(text):
    """
    Extract the candidate's name from the first non-empty line.
    """

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if line and len(line.split()) <= 4:
            return line

    return "Not Found"


def extract_email(text):
    """
    Extract email address from resume.
    """

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    match = re.findall(pattern, text)

    if match:
        return match[0]

    return "Not Found"


def extract_phone(text):
    """
    Extract Indian mobile number.
    """

    pattern = r'(?:\+91[- ]?)?[6-9]\d{9}'

    match = re.findall(pattern, text)

    if match:
        return match[0]

    return "Not Found"