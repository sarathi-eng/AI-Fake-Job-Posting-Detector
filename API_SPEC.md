# API Specification - Fake Job Posting Detector

## Base URL
```
http://localhost:8000
```

## Interactive API Documentation
When the server is running, visit: **http://localhost:8000/docs**

---

## Endpoints

### 1. Health Check
Check if the API is running.

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Fake Job Posting Detector",
  "version": "1.0.0"
}
```

---

### 2. Predict (Single Job)
Analyze a single job posting to determine if it's fake.

**Request:**
```
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Data Analyst",
  "company_name": "Google",
  "description": "Join our analytics team...",
  "salary_min": 800000,
  "salary_max": 1200000,
  "currency": "INR",
  "experience_required": "3-5 years",
  "job_type": "Full-time",
  "platform": "LinkedIn",
  "url": "https://linkedin.com/jobs/...",
  "company_website": "https://www.google.com",
  "location": "Bangalore, India"
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | ✓ | Job title |
| `company_name` | string | ✓ | Company name |
| `description` | string | ✓ | Job description text |
| `salary_min` | float | ✗ | Minimum salary |
| `salary_max` | float | ✗ | Maximum salary |
| `currency` | string | ✗ | Currency code (default: "INR") |
| `experience_required` | string | ✗ | e.g., "0-2 years", "5+ years" |
| `job_type` | string | ✗ | e.g., "Full-time", "Part-time" |
| `platform` | string | ✗ | e.g., "LinkedIn", "Indeed", "Internshala" |
| `url` | string | ✗ | Posting URL |
| `company_website` | string | ✗ | Company website URL |
| `location` | string | ✗ | Job location |

**Response:**
```json
{
  "classification": "Legitimate",
  "risk_score": 15.0,
  "confidence": 88.5,
  "reasons": [
    {
      "category": "text_pattern",
      "signal": "no_suspicious_keywords",
      "confidence": 0.9,
      "message": "No suspicious keywords detected"
    },
    {
      "category": "company",
      "signal": "verified_company",
      "confidence": 0.95,
      "message": "✓ Company found in verified databases"
    },
    {
      "category": "salary",
      "signal": "salary_realistic",
      "confidence": 0.85,
      "message": "✓ Salary range appears realistic for mid-level"
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `classification` | string | "Legitimate", "Suspicious", or "Fake" |
| `risk_score` | float | 0-100 (0=safe, 100=dangerous) |
| `confidence` | float | 0-100 (certainty of classification) |
| `reasons` | array | List of signals that contributed to the decision |

**Classification Logic:**
- **Risk ≥ 60**: 🔴 **FAKE** (immediately reject)
- **30 ≤ Risk < 60**: 🟡 **SUSPICIOUS** (review carefully)
- **Risk < 30**: 🟢 **LEGITIMATE** (likely safe)

---

### 3. Batch Predict
Analyze multiple job postings at once.

**Request:**
```
POST /batch-predict
Content-Type: application/json
```

**Request Body:**
```json
[
  {
    "title": "Job 1",
    "company_name": "Company A",
    "description": "...",
    "salary_min": 500000,
    "salary_max": 700000
  },
  {
    "title": "Job 2",
    "company_name": "Company B",
    "description": "...",
    "salary_min": 1000000,
    "salary_max": 1500000
  }
]
```

**Response:**
```json
{
  "predictions": [
    {
      "classification": "Legitimate",
      "risk_score": 12.0,
      "confidence": 87.0,
      "reasons": [...]
    },
    {
      "classification": "Fake",
      "risk_score": 72.0,
      "confidence": 94.0,
      "reasons": [...]
    }
  ],
  "total": 2
}
```

---

## Detection Signals

### Text Pattern Signals
Detected in job description text:

| Signal | Risk | Indicator |
|--------|------|-----------|
| `guaranteed_job` | CRITICAL | "Guaranteed job", "100% guarantee" |
| `no_interview` | CRITICAL | "No interview", "direct hiring" |
| `payment_required` | CRITICAL | "Registration fee", "processing fee" |
| `urgent_hiring` | HIGH | "Urgent hiring", "limited seats", "apply now" |
| `easy_money` | HIGH | "Easy money", "no experience required" |
| `personal_details_request` | CRITICAL | "Send Aadhar", "bank details" |
| `excessive_caps` | LOW | Excessive capitalization (>30%) |
| `excessive_punctuation` | LOW | Excessive punctuation (>10%) |
| `suspicious_emojis` | MEDIUM | Emojis in job description |
| `short_description` | LOW | Description <100 characters |

### Company Signals
Company verification:

| Signal | Impact |
|--------|--------|
| `verified_company` | ✓ Reduces risk |
| `website_found` | ✓ Neutral to positive |
| `no_website` | ✗ Increases risk |
| `not_in_registry` | ✗ Increases risk |

### Salary Signals
Compensation analysis:

| Signal | Condition |
|--------|-----------|
| `salary_realistic` | Within benchmarks |
| `salary_too_high` | 2x+ market standard |
| `salary_too_low` | <50% market standard |
| `no_salary` | Salary not provided |

---

## Error Responses

### 400 Bad Request
Invalid input data

```json
{
  "detail": "Validation error for job post fields"
}
```

### 500 Internal Server Error
Server processing error

```json
{
  "detail": "Error message describing the issue"
}
```

---

## Usage Examples

### Python
```python
import requests

url = "http://localhost:8000/predict"
job_post = {
    "title": "Senior Developer",
    "company_name": "Google",
    "description": "We are hiring senior developers...",
    "salary_min": 2000000,
    "salary_max": 3000000,
    "currency": "INR"
}

response = requests.post(url, json=job_post)
result = response.json()

print(f"Classification: {result['classification']}")
print(f"Risk Score: {result['risk_score']}")
```

### JavaScript
```javascript
const job = {
  title: "Data Scientist",
  company_name: "Microsoft",
  description: "Join our AI team...",
  salary_min: 1500000,
  salary_max: 2500000
};

fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(job)
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Engineer",
    "company_name": "Amazon",
    "description": "Hiring backend engineers...",
    "salary_min": 1800000,
    "salary_max": 2500000,
    "currency": "INR"
  }' | jq
```

---

## Weighting Algorithm

The final risk score combines three independent signals with weighted importance:

1. **Text Pattern Analysis** (50%): Detects scam keywords and suspicious writing patterns
2. **Company Verification** (30%): Validates company legitimacy
3. **Salary Anomaly Detection** (20%): Identifies unrealistic compensation

**Formula:**
```
Risk Score = (Text Risk × 0.50) + (Company Risk × 0.30) + (Salary Risk × 0.20)
Classification = Determine based on final risk score
```

Each signal contributes independently, and the algorithm prioritizes text-based scam indicators (most important) while also considering company reputation and salary realism.

---

## Performance Notes

- Single prediction: ~100-500ms
- Batch prediction (10 jobs): ~500-2000ms
- Company website verification uses timeout of 3 seconds
- All requests are processed synchronously

---

## Rate Limiting

Currently no rate limiting. In production, consider implementing:
- Max 100 requests per IP per minute
- Max 1000 requests per day per API key

---

## Future Enhancements

- [ ] Machine learning model training
- [ ] Cross-platform duplicate detection
- [ ] Real-time MCA/LinkedIn API integration
- [ ] Historical posting analysis
- [ ] Webhook notifications
- [ ] API authentication and rate limiting
- [ ] Caching for known companies

