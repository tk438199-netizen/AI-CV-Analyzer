import re
degree_database = [
    "Bachelor of Science",
    "BSc",
    "B.Sc",
    "Bachelor of Arts",
    "BA",
    "B.A",
    "Bachelor of Business Administration",
    "BBA",
    "Diploma in Engineering",
    "Diploma",
    "Higher Secondary Certificate",
    "HSC",
    "Secondary School Certificate",
    "SSC",
    "Master of Science",
    "MSc",
    "M.Sc",
    "Master of Arts",
    "MA",
    "PhD"
]


institution_database = [
    "Dhaka Polytechnic Institute",
    "Bangladesh University of Engineering and Technology",
    "Dhaka University",
    "University of Dhaka",
    "North South University",
    "BRAC University",
    "Daffodil International University",
    "American International University-Bangladesh",
    "Jahangirnagar University",
    "Chittagong University"
]


department_database = [
    "Computer Science and Technology",
    "Computer Science & Technology",
    "Computer Science",
    "Information Technology",
    "Electrical Engineering",
    "Electronics Engineering",
    "Civil Engineering",
    "Mechanical Engineering",
    "Computer Engineering",
    "Software Engineering"
]
def extract_degrees(text):

    found_degrees = []

    for degree in degree_database:

        pattern = (
            r'(?<![A-Za-z0-9])'
            + re.escape(degree)
            + r'(?![A-Za-z0-9])'
        )

        if re.search(pattern, text, re.IGNORECASE):

            found_degrees.append(degree)

    return found_degrees
def extract_institutions(text):

    found_institutions = []

    for institution in institution_database:

        pattern = re.escape(institution)

        if re.search(pattern, text, re.IGNORECASE):

            found_institutions.append(institution)

    return found_institutions
def extract_departments(text):

    found_departments = []

    for department in department_database:

        pattern = re.escape(department)

        if re.search(pattern, text, re.IGNORECASE):

            found_departments.append(department)

    return found_departments
def extract_passing_years(text):

    years = []

    education_pattern = (
        r'(?:education|academic qualification|'
        r'educational background|academic background)'
        r'([\s\S]*?)'
        r'(?=\n\s*(?:experience|skills|projects|'
        r'certifications|achievements)\b|$)'
    )

    match = re.search(
        education_pattern,
        text,
        re.IGNORECASE
    )

    if match:

        education_text = match.group(1)

        found_years = re.findall(
            r'\b(?:19|20)\d{2}\b',
            education_text
        )

        years = list(dict.fromkeys(found_years))

    return years
def extract_cgpa(text):

    pattern = (
        r'\b(?:CGPA|GPA)\s*[:=-]?\s*'
        r'(\d+(?:\.\d+)?\s*(?:/\s*\d+(?:\.\d+)?)?)'
    )

    results = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    return list(dict.fromkeys(results))
def analyze_education(text):

    education_data = {

        "degrees": extract_degrees(text),

        "institutions": extract_institutions(text),

        "departments": extract_departments(text),

        "passing_years": extract_passing_years(text),

        "cgpa": extract_cgpa(text)

    }

    return education_data