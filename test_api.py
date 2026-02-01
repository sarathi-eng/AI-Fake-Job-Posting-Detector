#!/usr/bin/env python3
"""Test the API with sample requests."""
import requests
import json

BASE_URL = "http://localhost:8000"

# Example fake job posting
fake_job = {
    "title": "Data Analyst",
    "company_name": "Tech Solutions Inc",
    "description": """
    GUARANTEED JOB!!! 🎉🎊
    
    NO INTERVIEW NEEDED!
    
    Earn ₹80,000/month from home with NO EXPERIENCE REQUIRED!!!
    
    Pay a ONE-TIME REGISTRATION FEE of ₹5,000 and get hired immediately.
    Limited seats available - APPLY NOW before it closes!
    """,
    "salary_min": 80_000,
    "salary_max": 80_000,
    "currency": "INR",
    "experience_required": "Fresher",
    "job_type": "Full-time",
    "platform": "LinkedIn",
    "location": "Remote",
}

# Example legitimate job
legit_job = {
    "title": "Senior Software Engineer",
    "company_name": "Google",
    "description": """
    Google is looking for a Senior Software Engineer to join our Cloud team.
    
    Responsibilities:
    - Design and build scalable systems
    - Mentor junior engineers
    - Contribute to open source
    
    Requirements:
    - 5+ years of software development experience
    - Strong knowledge of distributed systems
    - Experience with cloud platforms
    """,
    "salary_min": 2_500_000,
    "salary_max": 3_500_000,
    "currency": "INR",
    "experience_required": "5+ years",
    "job_type": "Full-time",
    "company_website": "https://www.google.com",
    "platform": "Google Careers",
    "location": "Bangalore, India",
}


def test_health():
    """Test the health endpoint."""
    print("\n" + "="*80)
    print("🔍 Testing Health Endpoint")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_fake_job():
    """Test detection on a fake job."""
    print("\n" + "="*80)
    print("🔍 Testing FAKE Job Detection")
    print("="*80)
    
    response = requests.post(f"{BASE_URL}/predict", json=fake_job)
    if response.status_code == 200:
        result = response.json()
        print(f"Classification: {result['classification']}")
        print(f"Risk Score: {result['risk_score']}/100")
        print(f"Confidence: {result['confidence']}%")
        print(f"\nReasons:")
        for i, reason in enumerate(result['reasons'][:5], 1):  # Show first 5 reasons
            print(f"  {i}. {reason['message']}")
        print("\n✅ API working correctly!" if result['classification'] == "Fake" else "⚠️ May need tuning")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False


def test_legit_job():
    """Test detection on a legitimate job."""
    print("\n" + "="*80)
    print("🔍 Testing LEGITIMATE Job Detection")
    print("="*80)
    
    response = requests.post(f"{BASE_URL}/predict", json=legit_job)
    if response.status_code == 200:
        result = response.json()
        print(f"Classification: {result['classification']}")
        print(f"Risk Score: {result['risk_score']}/100")
        print(f"Confidence: {result['confidence']}%")
        print(f"\nReasons (showing first 3):")
        for i, reason in enumerate(result['reasons'][:3], 1):
            print(f"  {i}. {reason['message']}")
        print("\n✅ Correct!" if result['classification'] == "Legitimate" else "⚠️ May need tuning")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False


def test_batch_predict():
    """Test batch prediction."""
    print("\n" + "="*80)
    print("🔍 Testing Batch Prediction")
    print("="*80)
    
    response = requests.post(f"{BASE_URL}/batch-predict", json=[fake_job, legit_job])
    if response.status_code == 200:
        result = response.json()
        print(f"Total predictions: {result['total']}")
        for i, pred in enumerate(result['predictions'], 1):
            print(f"\n  Job {i}: {pred.get('classification', 'ERROR')}")
            print(f"  Risk Score: {pred.get('risk_score', 'N/A')}/100")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False


if __name__ == "__main__":
    print("\n" + "█"*80)
    print("FAKE JOB POSTING DETECTOR - API TEST")
    print("█"*80)
    
    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Fake Job Detection", test_fake_job()))
    results.append(("Legitimate Job Detection", test_legit_job()))
    results.append(("Batch Prediction", test_batch_predict()))
    
    # Summary
    print("\n" + "█"*80)
    print("TEST SUMMARY")
    print("█"*80)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("✅ ALL TESTS PASSED" if all_passed else "⚠️ SOME TESTS FAILED"))
    print("█"*80 + "\n")
