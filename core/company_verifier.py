"""Company verification module."""
from __future__ import annotations

from typing import List, Tuple, Optional
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.settings import settings

MIN_REQUIRED_OVERLAP_SHORT = 1
MIN_REQUIRED_OVERLAP_LONG = 2
SHORT_NAME_TOKEN_THRESHOLD = 2


class CompanyVerifier:
    """Verifies company legitimacy through various sources."""

    def __init__(self):
        self.session = self._create_session()

    @staticmethod
    def _create_session():
        """Create a session with retry strategy."""
        session = requests.Session()
        retry = Retry(
            connect=3,
            read=3,
            status=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "HEAD"),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @staticmethod
    def _normalize_company_name(company_name: str) -> str:
        return " ".join(company_name.lower().strip().split())

    @staticmethod
    def _calculate_required_overlap(token_count: int) -> int:
        return (
            MIN_REQUIRED_OVERLAP_SHORT
            if token_count <= SHORT_NAME_TOKEN_THRESHOLD
            else MIN_REQUIRED_OVERLAP_LONG
        )

    def check_website_exists(self, company_name: str, website_url: Optional[str] = None) -> Tuple[bool, str]:
        """
        Check if company website is accessible.

        Returns (exists, reason).
        """
        if not website_url:
            normalized = self._normalize_company_name(company_name).replace(" ", "")
            website_url = f"https://{normalized}.com"

        parsed = urlparse(website_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return False, "Company website URL is invalid"

        try:
            response = self.session.head(website_url, timeout=3, allow_redirects=True)
            if response.status_code < 400:
                return True, f"Website accessible at {website_url}"
            return False, f"Website returned status {response.status_code}"
        except requests.RequestException:
            return False, "Website not accessible or unreachable"

    def check_company_in_registry(self, company_name: str) -> Tuple[bool, str]:
        """
        Check if company exists in a public registry (OpenCorporates).
        """
        normalized = self._normalize_company_name(company_name)
        if len(normalized) < 2 or normalized in {"company", "job", "hiring"}:
            return False, "Company name appears generic or suspicious"

        params = {
            "q": company_name,
            "order": "score",
            "per_page": 5,
            "inactive": "false",
        }
        if settings.company_registry_api_key:
            params["api_token"] = settings.company_registry_api_key

        try:
            response = self.session.get(
                settings.company_registry_api_url,
                params=params,
                timeout=5,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException:
            return False, "Company registry API unreachable"
        except ValueError:
            return False, "Company registry API returned invalid response"

        results = (
            payload.get("results", {})
            .get("companies", [])
        )

        if not results:
            return False, "Company not found in public registry"

        search_tokens = set(normalized.split())
        for item in results:
            company = item.get("company", {})
            candidate_name = self._normalize_company_name(company.get("name", ""))
            if not candidate_name:
                continue
            candidate_tokens = set(candidate_name.split())
            overlap = len(search_tokens & candidate_tokens)
            # Matching heuristic:
            # - Short names (1-2 tokens): 1 token overlap avoids over-rejecting valid firms.
            # - Longer names: 2 token overlap reduces false positives from generic words.
            # Example: "Apple" => 1 overlap; "Apple Inc" => 1 overlap; "Big Tech Solutions" => 2 overlaps.
            required_overlap = self._calculate_required_overlap(len(search_tokens))
            if overlap >= required_overlap:
                jurisdiction = company.get("jurisdiction_code", "unknown")
                return True, f"Found in public registry ({jurisdiction})"

        return False, "No close company match found in public registry"

    def calculate_company_score(self, company_name: str, website_url: Optional[str] = None) -> Tuple[float, List[dict]]:
        """
        Calculate risk score based on company verification.

        Returns (risk_score, reasons).
        """
        risk_score = 0.0
        reasons = []

        website_exists, website_msg = self.check_website_exists(company_name, website_url)
        if not website_exists:
            risk_score += 0.3
            reasons.append(
                {
                    "category": "company",
                    "signal": "no_website",
                    "confidence": 0.7,
                    "message": f"❌ {website_msg}",
                }
            )
        else:
            reasons.append(
                {
                    "category": "company",
                    "signal": "website_found",
                    "confidence": 0.8,
                    "message": f"✓ {website_msg}",
                }
            )

        in_registry, registry_msg = self.check_company_in_registry(company_name)
        if in_registry:
            reasons.append(
                {
                    "category": "company",
                    "signal": "verified_company",
                    "confidence": 0.9,
                    "message": f"✓ {registry_msg}",
                }
            )
            if website_exists:
                risk_score = max(risk_score - 0.1, 0.0)
        else:
            risk_score += 0.3 if not website_exists else 0.1
            reasons.append(
                {
                    "category": "company",
                    "signal": "not_in_registry",
                    "confidence": 0.65,
                    "message": f"❌ {registry_msg}",
                }
            )

        return min(max(risk_score, 0.0), 1.0), reasons
