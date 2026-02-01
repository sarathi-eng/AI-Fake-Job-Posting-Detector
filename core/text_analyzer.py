"""Text pattern analysis for detecting suspicious language."""
from typing import List, Tuple
import re


# Keywords and patterns associated with fake job postings
SCAM_KEYWORDS = {
    "guaranteed_job": [
        r"guaranteed\s+job",
        r"100%\s+job\s+guarantee",
        r"job\s+guaranteed",
    ],
    "no_interview": [
        r"no\s+interview",
        r"without\s+interview",
        r"direct\s+hiring",
        r"no\s+test",
    ],
    "payment_required": [
        r"registration\s+fee",
        r"processing\s+fee",
        r"security\s+deposit",
        r"pay\s+upfront",
        r"payment\s+required",
        r"refundable\s+deposit",
    ],
    "urgent_hiring": [
        r"urgent\s+hiring",
        r"limited\s+seats",
        r"immediate\s+opening",
        r"apply\s+now\s+before.*closed",
    ],
    "easy_money": [
        r"easy\s+money",
        r"earn\s+from\s+home",
        r"work\s+from\s+home\s+easy",
        r"no\s+experience\s+required",
        r"earn\s+₹.*without",
    ],
    "personal_details_request": [
        r"provide\s+bank\s+account",
        r"share\s+aadhar",
        r"personal\s+id\s+number",
        r"send\s+passport",
    ],
}


class TextAnalyzer:
    """Analyzes text for suspicious patterns."""

    @staticmethod
    def detect_scam_keywords(text: str) -> List[Tuple[str, List[str]]]:
        """
        Detect scam keywords in job description.
        
        Returns list of (category, matched_patterns).
        """
        text_lower = text.lower()
        results = []

        for category, patterns in SCAM_KEYWORDS.items():
            matched = []
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    matched.append(pattern)

            if matched:
                results.append((category, matched))

        return results

    @staticmethod
    def analyze_formatting(text: str) -> dict:
        """Analyze text formatting for suspicious markers."""
        metrics = {
            "excessive_caps": 0,
            "excessive_punctuation": 0,
            "suspicious_emojis": 0,
            "short_text": 0,
        }

        # Check for excessive caps
        if len(text) > 50:
            caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
            metrics["excessive_caps"] = caps_ratio if caps_ratio > 0.3 else 0

        # Check for excessive punctuation
        punct_count = sum(1 for c in text if c in "!?")
        punct_ratio = punct_count / max(len(text), 1)
        metrics["excessive_punctuation"] = punct_ratio if punct_ratio > 0.1 else 0

        # Check for suspicious emojis (common in scams)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "]+",
            flags=re.UNICODE,
        )
        metrics["suspicious_emojis"] = 1.0 if emoji_pattern.search(text) else 0

        # Check if text is too short for a real job posting
        metrics["short_text"] = 1.0 if len(text) < 100 else 0

        return metrics

    @staticmethod
    def calculate_text_score(text: str) -> Tuple[float, List[dict]]:
        """
        Calculate risk score based on text analysis.
        
        Returns (risk_score, reasons).
        """
        risk_score = 0.0
        reasons = []
        critical_keywords_count = 0

        # Check for scam keywords
        keywords_found = TextAnalyzer.detect_scam_keywords(text)
        for category, patterns in keywords_found:
            if category in ["payment_required", "personal_details_request", "guaranteed_job"]:
                # Critical signals - each one is very strong indicator of scam
                critical_keywords_count += 1
            
            reasons.append(
                {
                    "category": "text_pattern",
                    "signal": category,
                    "confidence": 0.85,
                    "message": f"Suspicious keyword detected: {category.replace('_', ' ')}",
                }
            )

        # If multiple critical keywords found, it's almost certainly fake
        if critical_keywords_count >= 2:
            risk_score += 0.75
        elif critical_keywords_count == 1:
            risk_score += 0.4
        
        # Each additional suspicious keyword adds to risk
        non_critical_count = len(keywords_found) - critical_keywords_count
        risk_score += min(non_critical_count * 0.1, 0.2)

        # Check formatting
        formatting = TextAnalyzer.analyze_formatting(text)
        if formatting["excessive_caps"] > 0:
            risk_score += 0.05
            reasons.append(
                {
                    "category": "text_pattern",
                    "signal": "excessive_caps",
                    "confidence": 0.5,
                    "message": "Text contains excessive capitalization",
                }
            )

        if formatting["excessive_punctuation"] > 0:
            risk_score += 0.05
            reasons.append(
                {
                    "category": "text_pattern",
                    "signal": "excessive_punctuation",
                    "confidence": 0.5,
                    "message": "Text contains excessive punctuation",
                }
            )

        if formatting["suspicious_emojis"] > 0:
            risk_score += 0.1
            reasons.append(
                {
                    "category": "text_pattern",
                    "signal": "suspicious_emojis",
                    "confidence": 0.7,
                    "message": "Text contains emojis (common in scam posts)",
                }
            )

        if formatting["short_text"] > 0:
            risk_score += 0.05
            reasons.append(
                {
                    "category": "text_pattern",
                    "signal": "short_description",
                    "confidence": 0.5,
                    "message": "Job description is unusually short",
                }
            )

        # Cap risk score at 1.0
        risk_score = min(risk_score, 1.0)
        return risk_score, reasons
