# 🚀 Getting Started Guide

## 5-Minute Quick Start

### Step 1: Setup (2 minutes)
```bash
cd "AI Fake Job Posting Detector"
bash setup.sh
```
This creates a virtual environment and installs dependencies.

### Step 2: Run Tests (1 minute)
```bash
source venv/bin/activate
python test_detector.py
```
You should see: `✅ ALL TESTS PASSED`

### Step 3: Start Server (1 minute)
```bash
source venv/bin/activate
python -m uvicorn api.main:app --reload
```
Server runs at: **http://localhost:8000**

### Step 4: Test API (1 minute)
Open a new terminal:
```bash
source venv/bin/activate
python test_api.py
```
You should see: `✅ ALL TESTS PASSED`

---

## 🐳 One-command run (recommended)

If you just want it to work without installing Python/Node manually:

```bash
docker compose up --build
```

Then open:
- Landing page: http://localhost:3000
- Swagger UI (paste JSON input here): http://localhost:8000/docs

---

## 🌐 Using the API

### Interactive Documentation
Open in browser: **http://localhost:8000/docs**

Try the API directly in your browser with Swagger UI!

### Example: Detect a Fake Job

**Using Python:**
```python
import requests

job = {
    "title": "Data Analyst",
    "company_name": "Unknown Company",
    "description": "GUARANTEED JOB!!! NO INTERVIEW! Pay ₹5000 fee!",
    "salary_min": 50000,
    "salary_max": 50000
}

response = requests.post("http://localhost:8000/predict", json=job)
result = response.json()

print(f"Classification: {result['classification']}")  # Output: Fake
print(f"Risk Score: {result['risk_score']}")          # Output: 68.0
for reason in result['reasons'][:3]:
    print(f"  - {reason['message']}")
```

**Using cURL:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Engineer",
    "company_name": "Google",
    "description": "Join our team...",
    "salary_min": 2000000,
    "salary_max": 3000000,
    "company_website": "https://www.google.com"
  }' | jq
```

**Using JavaScript:**
```javascript
const job = {
  title: "Backend Developer",
  company_name: "Microsoft",
  description: "Hiring experienced developers...",
  salary_min: 1800000,
  salary_max: 2500000
};

fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(job)
})
.then(res => res.json())
.then(data => {
  console.log(`Risk: ${data.risk_score}/100 - ${data.classification}`);
  data.reasons.forEach(r => console.log(`  • ${r.message}`));
});
```

---

## 🧩 Generate OpenAPI + Frontend Types

If you want a pinned API contract in the repo (useful for codegen and diffs), you can generate the OpenAPI spec and TypeScript types.

### Generate `openapi.json` (no server required)
```bash
source venv/bin/activate
python scripts/generate_openapi.py --out openapi.json
```

### Generate TypeScript types from OpenAPI (frontend)
```bash
npm run gen:api-types
```

This writes generated types to `lib/api/openapi.ts` and you can use the typed wrapper in `lib/api/client.ts`.

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete feature guide, troubleshooting, FAQ |
| **API_SPEC.md** | Full API documentation with all endpoints |
| **CURL_EXAMPLES.md** | Ready-to-copy cURL commands |
| **IMPLEMENTATION_SUMMARY.md** | Technical overview & architecture |
| **CHECKLIST.md** | Feature checklist & completion status |

---

## 🎯 Common Use Cases

### Use Case 1: Check a Single Job Posting
```python
# What: User wants to verify if a LinkedIn job is real
# How:
result = requests.post("http://localhost:8000/predict", json=job_data)
# Gets back: classification, risk_score, reasons
```

### Use Case 2: Batch Check Multiple Jobs
```python
# What: Platform wants to scan 100 new postings
# How:
result = requests.post("http://localhost:8000/batch-predict", json=jobs_list)
# Gets back: predictions for all jobs
```

### Use Case 3: Browser Extension
```javascript
// Content runs on job posting page
const jobText = document.body.innerText;
const company = document.querySelector('.company-name').text;
// Send to backend for analysis
// Show risk badge on the page
```

---

## 🔍 Understanding the Output

### Example Result (FAKE job):
```json
{
  "classification": "Fake",
  "risk_score": 68.0,
  "confidence": 66.4,
  "reasons": [
    {
      "category": "text_pattern",
      "signal": "guaranteed_job",
      "confidence": 0.85,
      "message": "Suspicious keyword detected: guaranteed job"
    },
    {
      "category": "text_pattern",
      "signal": "payment_required",
      "confidence": 0.85,
      "message": "Suspicious keyword detected: payment required"
    },
    {
      "category": "company",
      "signal": "no_website",
      "confidence": 0.7,
      "message": "❌ Website not accessible or unreachable"
    }
  ]
}
```

### Reading the Result:
- **Classification:** What we think (Legitimate/Suspicious/Fake)
- **Risk Score:** 0-100 (higher = more risky)
- **Confidence:** 0-100 (how sure we are)
- **Reasons:** Specific signals that led to this decision

### Decision Rules:
```
Risk >= 60    →  🔴 FAKE      (reject immediately)
30 ≤ Risk < 60 →  🟡 SUSPICIOUS (review carefully)
Risk < 30     →  🟢 LEGITIMATE  (likely safe)
```

---

## 🛠️ Troubleshooting

### Problem: "ModuleNotFoundError" when running tests
**Solution:** Make sure virtual environment is activated
```bash
source venv/bin/activate
```

### Problem: "Port 8000 already in use"
**Solution:** Use a different port
```bash
python -m uvicorn api.main:app --port 8001
```

### Problem: "Company not found" (everything flagged as no website)
**Solution:** This is normal for unknown companies. Add them to:
```python
# In core/company_verifier.py
known_companies = {
    "your_company": "Found in verified databases",
    # Add more...
}
```

### Problem: API tests fail
**Solution:** Make sure server is running in another terminal:
```bash
# Terminal 1:
python -m uvicorn api.main:app --reload

# Terminal 2:
python test_api.py
```

---

## 📊 What Gets Checked?

The detector automatically analyzes:

1. **Text Description**
   - Scam keywords (guaranteed, no interview, registration fee, etc.)
   - Formatting (excessive caps, punctuation, emojis)
   - Length (too short indicates low effort)

2. **Company Name**
   - Website existence & accessibility
   - Known/verified companies database
   - Generic or suspicious domain names

3. **Salary Information**
   - Realistic for role/experience
   - Market benchmarks by level
   - Currency support (INR)

4. **Metadata**
   - Platform (LinkedIn, Indeed, etc.)
   - URL
   - Location
   - Experience required

---

## 🎓 Learning the System

### How Scoring Works:
```
Final Risk Score = (Text Risk × 0.50) + (Company Risk × 0.30) + (Salary Risk × 0.20)
```

Each component independently calculates risk (0-1), then combined with weights.

### Example Calculation:
```
Text Analysis:    0.8 (multiple red flags)
Company Check:    0.3 (website not found)
Salary Check:     0.2 (realistic salary)

Final = (0.8 × 0.50) + (0.3 × 0.30) + (0.2 × 0.20)
      = 0.40 + 0.09 + 0.04
      = 0.53 × 100
      = 53 → Classification: SUSPICIOUS ✅
```

---

## 🚀 Next Steps

### To Extend the System:
1. **Add more companies** → Edit `core/company_verifier.py`
2. **Add more keywords** → Edit `core/text_analyzer.py`
3. **Add new test cases** → Edit `data/sample_jobs.py`
4. **Build a UI** → Create `frontend/` with React/Vue
5. **Deploy** → Docker + AWS/GCP/Azure

### To Integrate:
- **Browser Extension:** Inject detection script
- **Job Portal:** Call `/predict` API for each posting
- **Mobile App:** Use `/batch-predict` for efficiency
- **Monitoring System:** Track fraud trends over time

---

## 📞 Support

### Need Help?
1. Check [README.md](README.md) for full documentation
2. Check [API_SPEC.md](API_SPEC.md) for API details
3. Check [CURL_EXAMPLES.md](CURL_EXAMPLES.md) for command examples
4. Review test cases in `test_detector.py` and `test_api.py`

### Still Stuck?
- Review the code comments in `core/` modules
- Check console output for error messages
- Verify virtual environment is activated
- Ensure requirements.txt dependencies are installed

---

## ✨ Key Features at a Glance

✅ **Instant Detection** - Results in <500ms
✅ **Explainable** - Shows *why* a job is flagged
✅ **Multi-Signal** - Analyzes text, company, salary
✅ **Scalable** - Batch process multiple jobs
✅ **Easy Integration** - REST API with auto-docs
✅ **Well-Tested** - Comprehensive test coverage
✅ **Production-Ready** - Error handling, CORS, etc.

---

**Ready to protect job seekers? Start with `bash setup.sh`! 🎯**
