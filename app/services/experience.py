import re
from datetime import datetime

job_title_database = [

    "Python Developer",
    "Software Developer",
    "Software Engineer",
    "Web Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Java Developer",
    "Android Developer",
    "UI/UX Designer",
    "Graphic Designer",
    "Intern",
    "Teaching Assistant",
    "Research Assistant"

]

company_database = [

    "Google",
    "Microsoft",
    "Amazon",
    "Meta",
    "Apple",
    "IBM",
    "Oracle",
    "Samsung",
    "Tesla",
    "Infosys",
    "TCS",
    "Brain Station 23",
    "BJIT",
    "DataSoft"

]

def extract_job_titles(text):

    found_titles = []

    for title in job_title_database:

        pattern = re.escape(title)

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_titles.append(title)

    return found_titles
def extract_companies(text):

    found_companies = []

    for company in company_database:

        pattern = re.escape(company)

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_companies.append(company)

    return found_companies
def extract_employment_dates(text):

    date_pattern = (

        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|'
        r'Jul|Aug|Sep|Oct|Nov|Dec)'
        r'[a-z]*[\s,]+(?:19|20)\d{2}\b'

        r'|'

        r'\b(?:19|20)\d{2}[-/](?:0?[1-9]|1[0-2])\b'

    )

    dates = re.findall(
        date_pattern,
        text,
        re.IGNORECASE
    )

    return list(dict.fromkeys(dates))
def convert_to_month_year(date_text):

    date_text = date_text.strip()

    formats = [

        "%B %Y",
        "%b %Y",
        "%Y-%m",
        "%Y/%m"

    ]

    for date_format in formats:

        try:

            date = datetime.strptime(
                date_text,
                date_format
            )

            return date.year, date.month

        except ValueError:

            continue

    return None
def calculate_duration(start_date, end_date):

    start = convert_to_month_year(start_date)
    end = convert_to_month_year(end_date)

    if not start or not end:
        return 0

    start_year, start_month = start
    end_year, end_month = end

    total_months = (

        (end_year - start_year) * 12

        + (end_month - start_month)

    )

    return max(0, total_months)
def calculate_experience_years(total_months):

    years = total_months / 12

    return round(years, 2)

def analyze_experience(text):

    job_titles = extract_job_titles(text)

    companies = extract_companies(text)

    dates = extract_employment_dates(text)

    experience_data = {

        "has_experience": bool(
            job_titles or companies
        ),

        "job_titles": job_titles,

        "companies": companies,

        "employment_dates": dates,

        "total_experience_months": 0,

        "total_experience_years": 0.0

    }

    return experience_data
