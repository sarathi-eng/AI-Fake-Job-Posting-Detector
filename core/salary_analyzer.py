"""Salary anomaly detection module."""
from typing import List, Tuple, Optional


# Market salary ranges by role and experience (in INR)
SALARY_BENCHMARKS = {
    "fresher": {
        "entry_level": (250_000, 600_000),
        "internship": (0, 50_000),
    },
    "junior": {
        "1-3_years": (500_000, 1_000_000),
        "entry_level": (300_000, 800_000),
    },
    "mid": {
        "3-5_years": (1_000_000, 2_000_000),
        "4-6_years": (1_200_000, 2_200_000),
    },
    "senior": {
        "5-8_years": (1_500_000, 3_000_000),
        "8_plus_years": (2_500_000, 5_000_000),
    },
}


class SalaryAnalyzer:
    """Analyzes salary offers for anomalies."""

    @staticmethod
    def parse_experience_level(experience_str: Optional[str]) -> Optional[str]:
        """Map experience string to level."""
        if not experience_str:
            return None

        exp_lower = experience_str.lower()
        
        if "fresher" in exp_lower or "0" in exp_lower:
            return "fresher"
        elif "1" in exp_lower or "2" in exp_lower or "junior" in exp_lower:
            return "junior"
        elif "3" in exp_lower or "4" in exp_lower or "5" in exp_lower:
            return "mid"
        elif "senior" in exp_lower or "8" in exp_lower or "10" in exp_lower or "+" in exp_lower:
            return "senior"
        
        return None

    @staticmethod
    def get_salary_range(experience_level: Optional[str]) -> Optional[Tuple[float, float]]:
        """Get expected salary range for experience level."""
        if not experience_level:
            return None

        if experience_level in SALARY_BENCHMARKS:
            ranges = SALARY_BENCHMARKS[experience_level]
            # Return average range across all roles at this level
            all_mins = [r[0] for r in ranges.values()]
            all_maxs = [r[1] for r in ranges.values()]
            return (min(all_mins), max(all_maxs))
        
        return None

    @staticmethod
    def calculate_salary_score(
        salary_min: Optional[float],
        salary_max: Optional[float],
        experience: Optional[str],
        currency: Optional[str] = "INR",
    ) -> Tuple[float, List[dict]]:
        """
        Calculate risk score based on salary anomalies.
        
        Returns (risk_score, reasons).
        """
        risk_score = 0.0
        reasons = []

        # If no salary provided, skip this check
        if salary_min is None and salary_max is None:
            reasons.append(
                {
                    "category": "salary",
                    "signal": "no_salary",
                    "confidence": 0.4,
                    "message": "No salary information provided",
                }
            )
            return 0.1, reasons  # Slight penalty for missing salary

        # Currency check - if not INR, cannot verify against benchmarks
        if currency and currency.upper() != "INR":
            reasons.append(
                {
                    "category": "salary",
                    "signal": "non_inr_currency",
                    "confidence": 0.3,
                    "message": f"Salary in {currency} - cannot verify against local benchmarks",
                }
            )
            return 0.0, reasons

        # Parse experience level
        exp_level = SalaryAnalyzer.parse_experience_level(experience)
        expected_range = SalaryAnalyzer.get_salary_range(exp_level)

        if not expected_range:
            reasons.append(
                {
                    "category": "salary",
                    "signal": "unknown_experience",
                    "confidence": 0.3,
                    "message": "Could not determine experience level for salary comparison",
                }
            )
            return 0.0, reasons

        expected_min, expected_max = expected_range

        # Check if salary is unreasonably high
        salary_to_check = salary_max or salary_min
        if salary_to_check and salary_to_check > expected_max * 2:
            risk_score += 0.4
            reasons.append(
                {
                    "category": "salary",
                    "signal": "salary_too_high",
                    "confidence": 0.8,
                    "message": f"❌ Salary (₹{salary_to_check:,.0f}) is 2x higher than market standard for {exp_level}",
                }
            )
        # Check if salary is unreasonably low (but not zero)
        elif salary_to_check and salary_to_check > 0 and salary_to_check < expected_min * 0.5:
            risk_score += 0.2
            reasons.append(
                {
                    "category": "salary",
                    "signal": "salary_too_low",
                    "confidence": 0.6,
                    "message": f"⚠ Salary (₹{salary_to_check:,.0f}) is significantly below market rate for {exp_level}",
                }
            )
        else:
            reasons.append(
                {
                    "category": "salary",
                    "signal": "salary_realistic",
                    "confidence": 0.7,
                    "message": f"✓ Salary range appears realistic for {exp_level} level",
                }
            )

        return min(risk_score, 1.0), reasons
