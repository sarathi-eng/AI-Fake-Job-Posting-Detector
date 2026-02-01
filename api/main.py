"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import JobPost, PredictionResult
from core.detector import FakeJobDetector
from core.settings import settings

app = FastAPI(
    title="Fake Job Posting Detector",
    description="AI-powered system to detect fraudulent job postings",
    version="1.0.0",
)

# Enable CORS for browser-based requests
origins = settings.cors_origins_list()
allow_credentials = settings.cors_allow_credentials
if "*" in origins:
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=settings.cors_methods_list(),
    allow_headers=settings.cors_headers_list(),
)

# Initialize detector
detector = FakeJobDetector()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Fake Job Posting Detector",
        "version": "1.0.0",
    }


@app.post("/predict", response_model=PredictionResult)
async def predict_job_posting(job_post: JobPost) -> PredictionResult:
    """
    Detect if a job posting is fake.
    
    Input:
    - title: Job title
    - company_name: Name of the company
    - description: Full job description text
    - salary_min: Minimum salary (optional)
    - salary_max: Maximum salary (optional)
    - currency: Currency code (default: INR)
    - experience_required: Experience level (e.g., "0-2 years")
    - job_type: Type of job (e.g., "Full-time")
    - platform: Source platform (e.g., "LinkedIn")
    - url: URL of the posting (optional)
    - company_website: Company website URL (optional)
    - location: Job location (optional)
    
    Output:
    - classification: "Legitimate", "Suspicious", or "Fake"
    - risk_score: 0-100 (higher = more risk)
    - confidence: 0-100 (confidence in the classification)
    - reasons: List of specific signals/reasons for the classification
    """
    try:
        result = detector.predict(job_post)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-predict")
async def batch_predict(job_posts: list[JobPost]):
    """
    Detect if multiple job postings are fake.
    
    Input: List of JobPost objects
    
    Output: List of PredictionResult objects
    """
    results = []
    for job_post in job_posts:
        try:
            result = detector.predict(job_post)
            results.append(result)
        except Exception as e:
            results.append({
                "error": str(e),
                "job_title": job_post.title,
            })
    return {"predictions": results, "total": len(results)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
