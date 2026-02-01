"""Schemas for job posts and predictions."""
from typing import Optional, List
from pydantic import BaseModel


class JobPost(BaseModel):
    """Input schema for a job posting."""
    title: str
    company_name: str
    description: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = "INR"
    experience_required: Optional[str] = None  # e.g., "0-2 years", "5+ years"
    job_type: Optional[str] = None  # e.g., "Full-time", "Part-time", "Contract"
    platform: Optional[str] = None  # e.g., "LinkedIn", "Indeed", "Internshala"
    url: Optional[str] = None
    company_website: Optional[str] = None
    location: Optional[str] = None


class DetectionReason(BaseModel):
    """A single reason why a post might be fake."""
    category: str  # e.g., "text_pattern", "company", "salary", "cross_platform"
    signal: str  # specific trigger, e.g., "guaranteed_job", "company_not_found"
    confidence: float  # 0.0 to 1.0
    message: str  # human-readable explanation


class PredictionResult(BaseModel):
    """Output schema for fake job detection."""
    classification: str  # "Legitimate", "Suspicious", or "Fake"
    risk_score: float  # 0-100, where 100 is highest risk
    confidence: float  # 0-100, how certain we are
    reasons: List[DetectionReason]  # list of signals that triggered
