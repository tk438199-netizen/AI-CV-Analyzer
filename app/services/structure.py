import re

section_database = {

    "Personal Information": [
        "contact",
        "personal information",
        "personal details"
    ],

    "Professional Summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective"
    ],

    "Education": [
        "education",
        "academic qualification",
        "educational background"
    ],

    "Skills": [
        "skills",
        "technical skills",
        "key skills"
    ],

    "Experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history"
    ],

    "Projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "Certifications": [
        "certifications",
        "certificates",
        "licenses"
    ],

    "Achievements": [
        "achievements",
        "awards",
        "honors"
    ],

    "Languages": [
        "languages",
        "language proficiency"
    ]
}

def detect_sections(text):

    detected_sections = []

    text_lower = text.lower()

    for section, keywords in section_database.items():

        for keyword in keywords:

            pattern = (
                r'(?<![a-z0-9])'
                + re.escape(keyword)
                + r'(?![a-z0-9])'
            )

            if re.search(pattern, text_lower):

                detected_sections.append(section)

                break

    return detected_sections

def detect_missing_sections(detected_sections):

    missing_sections = []

    for section in section_database:

        if section not in detected_sections:

            missing_sections.append(section)

    return missing_sections

def calculate_structure_score(detected_sections):

    total_sections = len(section_database)

    available_sections = len(detected_sections)

    score = (
        available_sections / total_sections
    ) * 100

    return round(score, 2)

def analyze_word_count(text):

    words = re.findall(r'\b\w+\b', text)

    total_words = len(words)

    return total_words

def analyze_structure(text):

    detected_sections = detect_sections(text)

    missing_sections = detect_missing_sections(
        detected_sections
    )

    structure_score = calculate_structure_score(
        detected_sections
    )

    total_words = analyze_word_count(text)

    return {

        "detected_sections": detected_sections,

        "missing_sections": missing_sections,

        "total_sections": len(section_database),

        "detected_section_count": len(detected_sections),

        "structure_score": structure_score,

        "total_words": total_words

    }

