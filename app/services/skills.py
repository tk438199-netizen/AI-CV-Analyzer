import re
skills_database = {

    "Programming Languages": [
        "Python",
        "Java",
        "JavaScript",
        "C",
        "C++",
        "C#",
        "PHP",
        "TypeScript",
        "Ruby",
        "Go"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "React",
        "Next.js",
        "Node.js",
        "Express.js",
        "FastAPI",
        "Django",
        "Flask",
        "Bootstrap",
        "Tailwind CSS"
    ],

    "Database": [
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",
        "Oracle",
        "Redis"
    ],

    "Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Matplotlib"
    ],

    "Tools & Technologies": [
        "Git",
        "GitHub",
        "Docker",
        "Linux",
        "VS Code",
        "Jupyter Notebook",
        "Google Colab",
        "Postman"
    ]

}
def extract_skills(text):

    detected_skills = {}

    for category, skills in skills_database.items():

        found_skills = []

        for skill in skills:

            pattern = (
                r'(?<![A-Za-z0-9])'
                + re.escape(skill)
                + r'(?![A-Za-z0-9])'
            )

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            if matches:
                found_skills.append(skill)

        detected_skills[category] = found_skills

    return detected_skills
def count_total_skills(detected_skills):

    total = 0

    for category, skills in detected_skills.items():

        total += len(skills)

    return total
