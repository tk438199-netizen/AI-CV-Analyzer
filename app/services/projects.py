import re

project_section_keywords = [
    "projects",
    "personal projects",
    "academic projects",
    "professional projects",
    "key projects",
    "project experience"
]
def detect_project_section(text):

    text_lower = text.lower()

    for keyword in project_section_keywords:

        if keyword in text_lower:

            return True

    return False
technology_database = [

    "Python",
    "Java",
    "JavaScript",
    "C++",
    "HTML",
    "CSS",
    "React",
    "Next.js",
    "Node.js",
    "FastAPI",
    "Django",
    "Flask",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Machine Learning",
    "Deep Learning",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Git",
    "GitHub",
    "Docker",
    "Firebase",
    "Tailwind CSS"

]
def extract_technologies(text):

    found_technologies = []

    for technology in technology_database:

        pattern = (
            r'(?<![A-Za-z0-9])'
            + re.escape(technology)
            + r'(?![A-Za-z0-9])'
        )

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_technologies.append(technology)

    return found_technologies
def extract_project_links(text):

    github_pattern = (
        r'https?://(?:www\.)?github\.com/'
        r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+'
    )

    url_pattern = r'https?://[^\s<>]+'

    github_links = re.findall(
        github_pattern,
        text,
        re.IGNORECASE
    )

    all_links = re.findall(
        url_pattern,
        text,
        re.IGNORECASE
    )

    demo_links = []

    for link in all_links:

        if (
            "github.com" not in link.lower()
            and "linkedin.com" not in link.lower()
        ):

            demo_links.append(link.rstrip(".,;:)"))

    return {
        "github_links": list(dict.fromkeys(github_links)),
        "demo_links": list(dict.fromkeys(demo_links))
    }
def extract_project_section(text):

    pattern = (
        r'(?im)^[ \t]*'
        r'(?:personal projects|academic projects|'
        r'professional projects|key projects|projects)'
        r'[ \t]*:?[ \t]*\n'
        r'(.*?)'
        r'(?=^[ \t]*(?:education|experience|'
        r'work experience|skills|certifications|'
        r'achievements|languages|references)'
        r'[ \t]*:?[ \t]*$|\Z)'
    )

    match = re.search(
        pattern,
        text
    )

    if match:

        return match.group(1).strip()

    return ""
def count_projects(project_text):

    if not project_text:

        return 0

    lines = project_text.splitlines()

    count = 0

    for line in lines:

        line = line.strip()

        if (
            line
            and len(line.split()) <= 10
            and not line.endswith(".")
        ):

            count += 1

    return count
def analyze_projects(text):

    has_projects = detect_project_section(text)

    project_text = extract_project_section(text)

    technologies = extract_technologies(project_text)

    links = extract_project_links(project_text)

    total_projects = count_projects(project_text)

    return {

        "has_projects": has_projects,

        "total_projects": total_projects,

        "projects_section": project_text,

        "technologies": technologies,

        "technology_count": len(technologies),

        "github_links": links["github_links"],

        "demo_links": links["demo_links"]

    }
