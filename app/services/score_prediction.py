import joblib
import pandas as pd

from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():

    BASE_DIR = Path(__file__).resolve().parents[2]

    MODEL_PATH = BASE_DIR / "ml_model" / "cv_score_model.pkl"

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            "CV Score Model not found!"
        )

    model = joblib.load(MODEL_PATH)

    return model

def extract_features(
    personal_info,
    skills,
    education,
    experience,
    projects,
    certifications,
    structure
):

    skills_count = sum(
        len(skill_list)
        for skill_list in skills.values()
    )

    education_count = len(
        education.get("degrees", [])
    )

    experience_years = experience.get(
        "total_experience_years", 0.0
    )

    projects_count = projects.get(
        "total_projects", 0
    )

    certifications_count = certifications.get(
        "total_certifications", 0
    )

    has_summary = int(
        "Professional Summary"
        in structure.get("detected_sections", [])
    )

    has_contact_info = int(
        bool(
            personal_info.get("email")
            or personal_info.get("phone")
        )
    )

    has_github = int(
        bool(
            personal_info.get("github")
            or projects.get("github_links")
        )
    )

    structure_score = structure.get(
        "structure_score", 0
    )

    features = {

        "skills_count": skills_count,

        "education_count": education_count,

        "experience_years": experience_years,

        "projects_count": projects_count,

        "certifications_count": certifications_count,

        "has_summary": has_summary,

        "has_contact_info": has_contact_info,

        "has_github": has_github,

        "structure_score": structure_score

    }

    return features

def predict_cv_score(features):

    model = load_model()

    feature_df = pd.DataFrame(
        [features]
    )

    predicted_score = model.predict(
        feature_df
    )[0]

    predicted_score = max(
        0,
        min(100, predicted_score)
    )

    return round(float(predicted_score), 2)

