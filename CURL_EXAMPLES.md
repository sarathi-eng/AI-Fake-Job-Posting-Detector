# Example: Test the API with curl

# Health check
curl -X GET http://localhost:8000/health | jq

# Single prediction - FAKE job
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Data Analyst",
    "company_name": "Unknown Company",
    "description": "GUARANTEED JOB!!! NO INTERVIEW! Pay ₹5000 registration fee!",
    "salary_min": 100000,
    "salary_max": 100000,
    "currency": "INR",
    "experience_required": "Fresher"
  }' | jq

# Single prediction - LEGITIMATE job
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Engineer",
    "company_name": "Google",
    "description": "We are hiring senior engineers with 5+ years experience. Competitive salary and benefits.",
    "salary_min": 2500000,
    "salary_max": 3500000,
    "currency": "INR",
    "experience_required": "5+ years",
    "company_website": "https://www.google.com"
  }' | jq

# Batch prediction
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[
    {
      "title": "Job 1",
      "company_name": "Unknown",
      "description": "GUARANTEED MONEY!!!",
      "salary_min": 50000,
      "salary_max": 50000
    },
    {
      "title": "Job 2",
      "company_name": "Microsoft",
      "description": "Hiring software engineers",
      "salary_min": 2000000,
      "salary_max": 3000000,
      "company_website": "https://www.microsoft.com"
    }
  ]' | jq
