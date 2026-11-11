import re
certification_database = [
    "Python Programming",
    "Machine Learning",
    "Deep Learning",
    "Google Data Analytics",
    "AWS Certified",
    "AWS Cloud Practitioner",
    "Microsoft Azure",
    "Cisco Certified",
    "CCNA",
    "CCNP",
    "CompTIA A+",
    "CompTIA Security+",
    "Java Certification",
    "Web Development",
    "Data Science",
    "IELTS",
    "TOEFL",
    "IELTS Academic",
    "Professional Scrum Master",
    "Certified Ethical Hacker"
]

def extract_certifications(text):

    detected_certifications = []

    for certification in certification_database:

        pattern = (
            r'(?<![A-Za-z0-9])'
            + re.escape(certification)
            + r'(?![A-Za-z0-9])'
        )

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        if matches:
            detected_certifications.append(certification)

    return detected_certifications

def extract_certification_dates(text):

    date_pattern = (
        r'\b(?:'
        r'\d{1,2}[/-]\d{1,2}[/-]\d{4}'
        r'|'
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'[a-z]*\s+\d{4}'
        r'|'
        r'\d{4}'
        r')\b'
    )

    dates = re.findall(
        date_pattern,
        text,
        re.IGNORECASE
    )

    return list(set(dates))

def analyze_certifications(text):

    certifications = extract_certifications(text)

    dates = extract_certification_dates(text)

    return {
        "has_certifications": len(certifications) > 0,

        "total_certifications": len(certifications),

        "certifications": certifications,

        "dates": dates
    }

