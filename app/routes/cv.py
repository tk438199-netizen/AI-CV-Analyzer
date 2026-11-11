from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz
import re
from app.services.skills import (
    extract_skills,
    count_total_skills
)
from app.services.education import analyze_education
from app.services.experience import analyze_experience
router = APIRouter(
    prefix="/cv",
    tags=["CV Analysis"]
)
from app.services.projects import analyze_projects
from app.services.certifications import analyze_certifications
from app.services.structure import analyze_structure
from app.services.suggestions import generate_suggestions
from app.services.score_prediction import (
    extract_features,
    predict_cv_score
)
import json

from sqlalchemy.orm import Session

from fastapi import Depends

from app.database import get_db

from app.models.analysis import AnalysisHistory

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):

    # Check file extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    contents = await file.read()

    # Check file size (5 MB)
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    # Check empty file
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Open PDF from memory
    try:
        doc = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        # Extract text from all pages
        cv_text = ""

        for page in doc:
            cv_text += page.get_text() + "\n"

        page_count = len(doc)
        doc.close()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file"
        )

    # Clean extracted text
    clean_text = re.sub(
        r'\s+',
        ' ',
        cv_text
    ).strip()

    # Check extracted text
    if not clean_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text found. This PDF may require OCR."
        )

    # Count words
    word_count = len(clean_text.split())

    return {
        "message": "CV uploaded and processed successfully",
        "filename": file.filename,
        "page_count": page_count,
        "word_count": word_count,
        "extracted_text": clean_text
    }

def extract_personal_information(text):

    # Extract Email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    emails = re.findall(email_pattern, text)

    # Extract Phone Number
    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    phones = re.findall(phone_pattern, text)

    # Extract GitHub
    github_pattern = r'https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+'

    github = re.findall(
        github_pattern,
        text,
        re.IGNORECASE
    )

    # Extract LinkedIn
    linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+'

    linkedin = re.findall(
        linkedin_pattern,
        text,
        re.IGNORECASE
    )

    # Extract Name (basic heuristic)
    lines = text.split("\n")

    name = None

    for line in lines[:10]:

        line = line.strip()

        if (
            line
            and "@" not in line
            and not re.search(r'\d', line)
            and len(line.split()) <= 5
        ):
            name = line
            break

    return {
        "full_name": name,
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "github": github[0] if github else None,
        "linkedin": linkedin[0] if linkedin else None
    }

@router.post("/extract-personal-info")
async def extract_personal_info_api(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read file
    contents = await file.read()

    # Validate file size
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract PDF text
    try:
        doc = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        cv_text = ""

        for page in doc:
            cv_text += page.get_text() + "\n"

        doc.close()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF"
        )

    if not cv_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Extract personal information
    personal_info = extract_personal_information(cv_text)

    return {
        "message": "Personal information extracted successfully",
        "filename": file.filename,
        "personal_information": personal_info
    }

@router.post("/extract-skills")
async def extract_skills_api(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    contents = await file.read()

    # Validate file size
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract PDF text
    try:

        doc = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        cv_text = ""

        for page in doc:
            cv_text += page.get_text() + "\n"

        doc.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF"
        )

    if not cv_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Extract skills
    detected_skills = extract_skills(cv_text)

    # Count total skills
    total_skills = count_total_skills(detected_skills)

    return {
        "message": "Skills extracted successfully",
        "filename": file.filename,
        "total_skills": total_skills,
        "skills": detected_skills
    }
@router.post("/extract-education")
async def extract_education_api(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    contents = await file.read()

    # Validate file size
    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract PDF text
    try:

        doc = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        cv_text = ""

        for page in doc:

            cv_text += page.get_text() + "\n"

        doc.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF"
        )

    # Check extracted text
    if not cv_text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Analyze education
    education_data = analyze_education(cv_text)

    return {

        "message": "Education information extracted successfully",

        "filename": file.filename,

        "education": education_data

    }@router.post("/extract-experience")
async def extract_experience_api(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    contents = await file.read()

    # Validate file size
    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract PDF text
    try:

        doc = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        cv_text = ""

        for page in doc:

            cv_text += page.get_text() + "\n"

        doc.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF"
        )

    # Check extracted text
    if not cv_text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Analyze experience
    experience_data = analyze_experience(cv_text)

    return {

        "message": "Experience information extracted successfully",

        "filename": file.filename,

        "experience": experience_data

    }

@router.post("/extract-projects")
async def extract_projects_api(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    contents = await file.read()

    # Validate file size
    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract PDF text
    try:

        doc = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        cv_text = ""

        for page in doc:

            cv_text += page.get_text() + "\n"

        doc.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF"
        )

    # Check extracted text
    if not cv_text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Analyze projects
    project_data = analyze_projects(cv_text)

    return {

        "message": "Project information extracted successfully",

        "filename": file.filename,

        "projects": project_data

    }

@router.post("/extract-certifications")
async def extract_cv_certifications(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5MB"
        )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    try:

        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        text = ""

        for page in pdf_document:
            text += page.get_text() + "\n"

        pdf_document.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read PDF file"
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    result = analyze_certifications(text)

    return {
        "filename": file.filename,
        "certification_analysis": result
    }

@router.post("/analyze-structure")
async def analyze_cv_structure(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    try:

        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        text = ""

        for page in pdf_document:

            text += page.get_text() + "\n"

        pdf_document.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read PDF file"
        )

    if not text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    result = analyze_structure(text)

    return {

        "filename": file.filename,

        "structure_analysis": result

    }

@router.post("/improvement-suggestions")
async def cv_improvement_suggestions(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    try:

        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        text = ""

        for page in pdf_document:

            text += page.get_text() + "\n"

        pdf_document.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read PDF file"
        )

    if not text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Extract all information

    personal_info = extract_personal_information(text)

    skills = extract_skills(text)

    education = analyze_education(text)

    experience = analyze_experience(text)

    projects = analyze_projects(text)

    certifications = analyze_certifications(text)

    structure = analyze_structure(text)

    # Generate suggestions

    result = generate_suggestions(
        personal_info,
        skills,
        education,
        experience,
        projects,
        certifications,
        structure
    )

    return {
        "filename": file.filename,
        "improvement_analysis": result
    }

@router.post("/predict-score")
async def predict_score(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    try:

        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        text = ""

        for page in pdf_document:

            text += page.get_text() + "\n"

        pdf_document.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read PDF file"
        )

    if not text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # Extract CV Information

    personal_info = extract_personal_information(text)

    skills = extract_skills(text)

    education = analyze_education(text)

    experience = analyze_experience(text)

    projects = analyze_projects(text)

    certifications = analyze_certifications(text)

    structure = analyze_structure(text)

    # Extract ML Features

    features = extract_features(
        personal_info,
        skills,
        education,
        experience,
        projects,
        certifications,
        structure
    )

    # Predict CV Score

    try:

        score = predict_cv_score(features)

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="CV score prediction failed"
        )

    return {

        "filename": file.filename,

        "predicted_cv_score": score,

        "score_out_of": 100,

        "features_used": features

    }

@router.post("/analyze-complete")
async def complete_cv_analysis(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1. Validate PDF

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5MB"
        )

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # 2. Extract PDF Text

    try:

        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        text = ""

        for page in pdf_document:

            text += page.get_text() + "\n"

        page_count = len(pdf_document)

        pdf_document.close()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read PDF file"
        )

    if not text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in PDF"
        )

    # 3. Personal Information

    personal_info = extract_personal_information(text)

    # 4. Skills Analysis

    skills = extract_skills(text)

    # 5. Education Analysis

    education = analyze_education(text)

    # 6. Experience Analysis

    experience = analyze_experience(text)

    # 7. Projects Analysis

    projects = analyze_projects(text)

    # 8. Certifications Analysis

    certifications = analyze_certifications(text)

    # 9. Structure Analysis

    structure = analyze_structure(text)

    # 10. Improvement Suggestions

    suggestions = generate_suggestions(
        personal_info,
        skills,
        education,
        experience,
        projects,
        certifications,
        structure
    )

    # 11. Feature Extraction

    features = extract_features(
        personal_info,
        skills,
        education,
        experience,
        projects,
        certifications,
        structure
    )

    # 12. CV Score Prediction

    try:

        predicted_score = predict_cv_score(features)

    except FileNotFoundError:

        raise HTTPException(
            status_code=503,
            detail="CV Score Model not found"
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="CV Score Prediction Failed"
        )

    # 13. Final Response

    result = {

    "message": "CV Analysis Completed Successfully",

    "filename": file.filename,

    "file_information": {

        "page_count": page_count,

        "word_count": structure["total_words"]

    },

    "personal_information": personal_info,

    "skills_analysis": {

        "skills": skills,

        "total_skills": sum(
            len(skill_list)
            for skill_list in skills.values()
        )

    },

    "education_analysis": education,

    "experience_analysis": experience,

    "projects_analysis": projects,

    "certifications_analysis": certifications,

    "structure_analysis": structure,

    "improvement_analysis": suggestions,

    "score_analysis": {

        "predicted_score": predicted_score,

        "score_out_of": 100,

        "features_used": features

    }

}

# Save Analysis in Database

    try:
        new_analysis = AnalysisHistory(
                filename=file.filename,
                page_count=page_count,
                word_count=structure["total_words"],
                predicted_score=predicted_score,
                analysis_result=json.dumps(result)
            )
        
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        
    except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to save analysis history"
            )
        
    result["analysis_id"] = new_analysis.id
        
    return result

@router.get("/history")
def get_analysis_history(db: Session = Depends(get_db)):

    history = (
        db.query(AnalysisHistory)
        .order_by(AnalysisHistory.created_at.desc())
        .all()
    )

    return {

        "total_records": len(history),

        "history": [

            {
                "id": item.id,

                "filename": item.filename,

                "page_count": item.page_count,

                "word_count": item.word_count,

                "predicted_score": item.predicted_score,

                "created_at": item.created_at

            }

            for item in history

        ]

    }

@router.get("/history/{analysis_id}")
def get_analysis_details(
    analysis_id: int,
    db: Session = Depends(get_db)
):

    analysis = db.query(AnalysisHistory).filter(
        AnalysisHistory.id == analysis_id
    ).first()

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Analysis history not found"
        )

    return {

        "id": analysis.id,

        "filename": analysis.filename,

        "created_at": analysis.created_at,

        "analysis": json.loads(
            analysis.analysis_result
        )

    }

