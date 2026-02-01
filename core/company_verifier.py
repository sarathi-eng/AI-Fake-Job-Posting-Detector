"""Company verification module."""
from typing import List, Tuple, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class CompanyVerifier:
    """Verifies company legitimacy through various sources."""

    def __init__(self):
        self.session = self._create_session()

    @staticmethod
    def _create_session():
        """Create a session with retry strategy."""
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def check_website_exists(self, company_name: str, website_url: Optional[str] = None) -> Tuple[bool, str]:
        """
        Check if company website is accessible.
        
        Returns (exists, reason).
        """
        if not website_url:
            # Try to guess URL from company name
            website_url = f"https://{company_name.lower().replace(' ', '')}.com"

        # Check if it's a known fake/generic domain
        if any(fake_indicator in website_url.lower() for fake_indicator in [
            "techsolutionsinc",
            "unknownstartup",
            "xyzconsultancy",
            "fakecompany",
            "test.com",
        ]):
            return False, "Website domain appears generic or unregistered"

        try:
            response = self.session.head(website_url, timeout=3, allow_redirects=True)
            if response.status_code < 400:
                return True, f"Website accessible at {website_url}"
            else:
                return False, f"Website returned status {response.status_code}"
        except requests.RequestException:
            return False, f"Website not accessible or unreachable"

    def check_company_in_registry(self, company_name: str) -> Tuple[bool, str]:
        """
        Check if company exists in trusted registries (MCA, etc).
        This is a stub - in production, would connect to real APIs.
        """
        # Known legitimate companies (demo data)
        known_companies = {
            "google": "Found in verified databases",
            "microsoft": "Found in verified databases",
            "amazon": "Found in verified databases",
            "apple": "Found in verified databases",
            "meta": "Found in verified databases",
            "infosys": "Found in verified databases",
            "tcs": "Found in verified databases",
            "wipro": "Found in verified databases",
            "accenture": "Found in verified databases",
        }

        company_lower = company_name.lower().strip()
        if company_lower in known_companies:
            return True, known_companies[company_lower]

        # Check if company name looks suspicious
        if len(company_lower) < 2 or company_lower in ["company", "job", "hiring"]:
            return False, "Company name appears generic or suspicious"

        # For unknown companies, return neutral
        return False, "Company not found in verified databases"

    def calculate_company_score(self, company_name: str, website_url: Optional[str] = None) -> Tuple[float, List[dict]]:
        """
        Calculate risk score based on company verification.
        
        Returns (risk_score, reasons).
        """
        risk_score = 0.0
        reasons = []

        # Check website
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

        # Check company registry
        in_registry, registry_msg = self.check_company_in_registry(company_name)
        if not in_registry and website_exists is False:
            risk_score += 0.3
            reasons.append(
                {
                    "category": "company",
                    "signal": "not_in_registry",
                    "confidence": 0.6,
                    "message": f"❌ {registry_msg}",
                }
            )
        elif in_registry:
            reasons.append(
                {
                    "category": "company",
                    "signal": "verified_company",
                    "confidence": 0.9,
                    "message": f"✓ {registry_msg}",
                }
            )

        return min(risk_score, 1.0), reasons
