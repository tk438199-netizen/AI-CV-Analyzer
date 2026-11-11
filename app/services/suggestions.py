def generate_suggestions(
    personal_info,
    skills,
    education,
    experience,
    projects,
    certifications,
    structure
):


    suggestions = []

    # 1. Personal Information Suggestions

    if not personal_info.get("email"):

        suggestions.append(
            "Add a professional email address to your CV."
        )

    if not personal_info.get("phone"):

        suggestions.append(
            "Add your contact number to your CV."
        )

    if not personal_info.get("github"):

        suggestions.append(
            "Add your GitHub profile link to showcase your coding projects."
        )

    if not personal_info.get("linkedin"):

        suggestions.append(
            "Add your LinkedIn profile to improve your professional presence."
        )

    # 2. Skills Suggestions

    total_skills = sum(
        len(skill_list)
        for skill_list in skills.values()
    )

    if total_skills == 0:

        suggestions.append(
            "Add relevant technical and professional skills."
        )

    elif total_skills < 5:

        suggestions.append(
            "Consider adding more relevant skills to your CV."
        )

    # 3. Education Suggestions

    if not education.get("degrees"):

        suggestions.append(
            "Add your educational qualifications."
        )

    if not education.get("institutions"):

        suggestions.append(
            "Mention the names of your educational institutions."
        )

    # 4. Experience Suggestions

    if not experience.get("has_experience"):

        suggestions.append(
            "Consider adding relevant internship, volunteer, or work experience if available."
        )

    # 5. Projects Suggestions

    if not projects.get("has_projects"):

        suggestions.append(
            "Add personal or academic projects to demonstrate practical skills."
        )

    if not projects.get("github_links"):

        suggestions.append(
            "Include GitHub repository links for your projects when available."
        )

    # 6. Certifications Suggestions

    if not certifications.get("has_certifications"):

        suggestions.append(
            "Add relevant certifications or completed training courses if available."
        )

    # 7. Structure Suggestions

    missing_sections = structure.get(
        "missing_sections", []
    )

    for section in missing_sections:

        suggestions.append(
            f"Consider adding a {section} section to your CV if relevant."
        )

    # 8. Word Count Suggestions

    total_words = structure.get("total_words", 0)

    if total_words < 150:

        suggestions.append(
            "Your CV contains very little text. Add relevant details about your education, skills, and projects."
        )

    elif total_words > 1000:

        suggestions.append(
            "Your CV may be too lengthy. Consider removing unnecessary information."
        )

    # Final Result

    if not suggestions:

        suggestions.append(
            "Your CV covers the main areas checked by this system. Review it for accuracy and relevance."
        )

    return {
        "total_suggestions": len(suggestions),
        "suggestions": suggestions
    }