"""Main detection engine that combines all signals."""
from typing import List
from core.schemas import JobPost, PredictionResult, DetectionReason
from core.text_analyzer import TextAnalyzer
from core.company_verifier import CompanyVerifier
from core.salary_analyzer import SalaryAnalyzer


class FakeJobDetector:
    """Main detector combining all analysis modules."""

    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.company_verifier = CompanyVerifier()
        self.salary_analyzer = SalaryAnalyzer()

    def predict(self, job_post: JobPost) -> PredictionResult:
        """
        Predict if a job posting is fake.
        
        Args:
            job_post: JobPost instance with job details
            
        Returns:
            PredictionResult with classification, risk score, and reasons
        """
        all_reasons: List[DetectionReason] = []
        weighted_risk_score = 0.0
        total_weight = 0.0

        # 1. Text Pattern Analysis (50% weight - most critical for scam detection)
        text_risk, text_reasons = self.text_analyzer.calculate_text_score(
            job_post.description
        )
        weighted_risk_score += text_risk * 0.50
        total_weight += 0.50
        for reason in text_reasons:
            all_reasons.append(DetectionReason(**reason))

        # 2. Company Verification (30% weight)
        company_risk, company_reasons = self.company_verifier.calculate_company_score(
            job_post.company_name, job_post.company_website
        )
        weighted_risk_score += company_risk * 0.30
        total_weight += 0.30
        for reason in company_reasons:
            all_reasons.append(DetectionReason(**reason))

        # 3. Salary Anomaly Detection (20% weight)
        salary_risk, salary_reasons = self.salary_analyzer.calculate_salary_score(
            job_post.salary_min,
            job_post.salary_max,
            job_post.experience_required,
            job_post.currency,
        )
        weighted_risk_score += salary_risk * 0.20
        total_weight += 0.20
        for reason in salary_reasons:
            all_reasons.append(DetectionReason(**reason))

        # Calculate weighted risk score (0-1) and convert to percentage
        final_risk_score = weighted_risk_score / total_weight if total_weight > 0 else 0.0
        risk_score_percent = final_risk_score * 100

        # Determine classification based on risk score with adjusted thresholds
        if risk_score_percent >= 60:
            classification = "Fake"
            confidence = min(98, 60 + (risk_score_percent - 60) * 0.8)
        elif risk_score_percent >= 30:
            classification = "Suspicious"
            confidence = 50 + (risk_score_percent - 30) * 0.8
        else:
            classification = "Legitimate"
            confidence = max(55, 85 - risk_score_percent)

        return PredictionResult(
            classification=classification,
            risk_score=round(risk_score_percent, 2),
            confidence=round(confidence, 2),
            reasons=all_reasons,
        )
