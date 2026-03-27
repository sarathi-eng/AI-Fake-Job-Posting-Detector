# 🚨 Fake Job Posting Detector

An AI-powered system to automatically detect fraudulent job postings across all major job platforms (LinkedIn, Indeed, Internshala, company career pages, etc.). Protects job seekers from scams by analyzing multiple signals and providing transparent, explainable risk assessments.

---

## 🎯 Features

### 1. **Text Pattern Analysis**
Detects suspicious language patterns commonly found in scam postings:
- "Guaranteed job", "No interview", "Pay registration fee"
- "Urgent hiring – limited seats"
- Excessive capitalization, punctuation, emojis
- Unusually short or vague descriptions

### 2. **Company Verification**
Validates company legitimacy:
- ✓ Checks if company website exists and is accessible
- ✓ Cross-references with trusted databases (MCA, LinkedIn, etc.)
- ✓ Flags newly created or unverifiable companies

### 3. **Salary & Offer Anomaly Detection**
Identifies unrealistic compensation:
- Compares salary to industry benchmarks
- Flags salaries 2x+ higher than market standard for role/experience
- Detects extremely low salaries or incomplete offers

### 4. **Risk Classification & Explainability**
Provides transparent outputs:
- **Classification**: "Legitimate", "Suspicious", or "Fake"
- **Risk Score**: 0-100 (higher = more risk)
- **Confidence**: How certain the system is
- **Reasons**: Human-readable explanations for each signal

### 5. **Multi-Platform Compatibility**
Can be deployed as:
- REST API (this implementation)
- Browser extension
- Standalone web application
- Integration with job portals

---

## 🏗️ Project Structure

```
├── api/
│   ├── main.py                 # FastAPI application with endpoints
│   └── __init__.py
├── core/
│   ├── __init__.py
│   ├── schemas.py              # Pydantic models for input/output
│   ├── text_analyzer.py        # Text pattern detection
│   ├── company_verifier.py     # Company verification logic
│   ├── salary_analyzer.py      # Salary anomaly detection
│   └── detector.py             # Main detection engine
├── data/
│   └── sample_jobs.py          # Test job postings (fake, legit, suspicious)
├── frontend/                   # Flattened UI source from old my-app/apps/web
├── models/                     # Trained sklearn model artifact(s)
├── scripts/
│   └── train_emscad_model.py   # Train model from EMSCAD Kaggle dataset
├── .github/workflows/ci.yml    # CI for detector and API tests
├── test_detector.py            # Quick test script
├── test_api.py                 # API smoke/integration test script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone/navigate to project
cd "AI Fake Job Posting Detector"

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Run Tests**

```bash
python test_detector.py
```

Expected output:
```
🔍 TEST 1: FAKE JOB (Guaranteed money + payment required)
Classification: Fake
Risk Score: 85.0/100
Confidence: 92.5%

🔍 TEST 4: LEGITIMATE JOB (Google - verified company)
Classification: Legitimate
Risk Score: 10.0/100
Confidence: 85.0%
```

### 3. **Start the API Server**

```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

---

## ✅ Easiest way for anyone (Docker)

If you want a one-command setup that works the same on any machine:

```bash
docker compose up --build
```

Open:
- Landing page: `http://localhost:3000`
- Swagger UI (input form): `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

More details: see `DEPLOYMENT.md`.

---

## 🌐 Landing Page (Production-style, No Demo)

This repo also includes a minimal Next.js landing page (Hero/Features/API/Example Output/Footer). It does **not** include an interactive demo UI.

```bash
npm install
npm run dev
```

Open: `http://localhost:3000`

If your API is running somewhere else, set:

```bash
export NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
```

---

## 🎥 Live Demo

![Live demo](assets/demo.gif)

> Temporary placeholder. Replace `assets/demo.gif` with a real walkthrough recording before release.

---

## 🏷️ Suggested Repository Topics

`fraud-detection`, `nlp`, `machine-learning`, `fastapi`, `job-scam`

---

## 📡 API Usage

### **GET /health**
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Fake Job Posting Detector",
  "version": "1.0.0"
}
```

---

### **POST /predict**
Predict if a single job posting is fake.

**Request Body:**
```json
{
  "title": "Data Analyst",
  "company_name": "Google",
  "description": "Join our data team...",
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
      "message": "✓ No suspicious keywords detected"
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

---

### **POST /batch-predict**
Predict multiple job postings at once.

**Request Body:**
```json
[
  {
    "title": "Job 1",
    "company_name": "Company A",
    "description": "...",
    ...
  },
  {
    "title": "Job 2",
    "company_name": "Company B",
    "description": "...",
    ...
  }
]
```

**Response:**
```json
{
  "predictions": [
    { "classification": "Legitimate", "risk_score": 12.0, ... },
    { "classification": "Fake", "risk_score": 88.0, ... }
  ],
  "total": 2
}
```

---

## 🧪 Example Predictions

### ❌ FAKE Posting
```
Title: Data Analyst
Company: Tech Solutions Inc
Description: "GUARANTEED JOB!!! Pay ₹5,000 registration fee, NO INTERVIEW, Earn ₹80,000/month..."

Classification: FAKE
Risk Score: 85.0/100
Confidence: 92.5%

Reasons:
✗ Guaranteed job keyword detected
✗ Payment required for job
✗ No interview claim (suspicious)
✗ Salary unusually high for fresher
✗ Company not found in trusted databases
```

### ⚠️ SUSPICIOUS Posting
```
Title: Business Analyst
Company: Unknown Startup XYZ
Description: "Urgent hiring... [normal description]"

Classification: SUSPICIOUS
Risk Score: 45.0/100
Confidence: 72.0%

Reasons:
⚠ Company not found in verified databases
⚠ Website not accessible
✓ Salary appears realistic
✓ No suspicious keywords in description
```

### ✅ LEGITIMATE Posting
```
Title: Senior Software Engineer
Company: Google
Description: "Google is hiring... [detailed description]"

Classification: LEGITIMATE
Risk Score: 8.0/100
Confidence: 92.0%

Reasons:
✓ Company verified (Google)
✓ Official website accessible
✓ Salary within market range
✓ Professional description
✓ No scam indicators detected
```

---

## 🔧 Detection Signals Explained

### **Text Pattern Signals**
| Signal | Risk | Example |
|--------|------|---------|
| `guaranteed_job` | HIGH | "100% job guarantee" |
| `no_interview` | HIGH | "Direct hiring, no interview" |
| `payment_required` | CRITICAL | "₹5,000 registration fee" |
| `urgent_hiring` | MEDIUM | "Urgent hiring, limited seats" |
| `easy_money` | HIGH | "Earn ₹100k working 1 hour/day" |
| `personal_details_request` | CRITICAL | "Send your Aadhar number" |
| `excessive_caps` | LOW | "APPLY NOW!!!" |
| `suspicious_emojis` | MEDIUM | "🎉🎊💰" |
| `short_description` | LOW | Very brief job description |

### **Company Signals**
| Signal | Impact |
|--------|--------|
| `verified_company` | Reduces risk |
| `website_found` | Neutral to positive |
| `no_website` | Increases risk |
| `not_in_registry` | Increases risk (if no website) |

### **Salary Signals**
| Signal | Condition |
|--------|-----------|
| `salary_realistic` | Within benchmarks for role/exp |
| `salary_too_high` | 2x+ market standard |
| `salary_too_low` | <50% market standard |
| `no_salary` | Not provided |

---

## 📊 Scoring Algorithm

**Risk Score Calculation:**
1. **Rule-based block** (0-1.0): weighted within rules
   - Text analysis: 50%
   - Company verification: 30%
   - Salary analysis: 20%
2. **ML fraud probability** (0-1.0): scikit-learn model trained on EMSCAD
3. **Weighted ensemble**:
   - Final risk = `0.60 × rule_risk + 0.40 × ml_probability` (when model is available)
   - Fallback = rule-only risk (when model file is missing or disabled)
4. **Final score** = risk × 100

**Classification Rules:**
- **Risk ≥ 60**: 🔴 **FAKE** (high confidence)
- **30 ≤ Risk < 60**: 🟡 **SUSPICIOUS** (medium confidence)
- **Risk < 30**: 🟢 **LEGITIMATE** (high confidence)

These thresholds were re-tuned for the ensemble (from 70/40 to 60/30) to preserve practical detector behavior on the existing sample tests after adding ML probability as a second signal.

---

## 🧠 ML Training (EMSCAD Kaggle Dataset)

Train the text classifier from an EMSCAD CSV:

```bash
python scripts/train_emscad_model.py --dataset /path/to/fake_job_postings.csv --out models/fake_job_classifier.joblib
```

Expected target column: `fraudulent`.

---

## 🔮 Future Enhancements

### Near-term
- [ ] Browser extension for Chrome/Firefox
- [ ] LinkedIn integration (check against company careers page)
- [ ] Database of known scam companies
- [ ] Historical posting analysis (detect cloned listings)

### Medium-term
- [ ] NLP models for writing style analysis (BERT, GPT)
- [ ] Integration with job portal APIs
- [ ] Real-time company registry checks (MCA, SEBI)
- [ ] Salary survey data integration

### Long-term
- [ ] Cross-platform aggregation (detect scammers across portals)
- [ ] User feedback loop (improve model with verified data)
- [ ] Scam report database (community-driven)
- [ ] Blockchain-based company verification

---

## 🤝 Contributing

Ideas for improvement:
1. Add more scam keyword patterns
2. Integrate real company verification APIs
3. Implement ML-based text classification
4. Add more salary benchmarks by role/location
5. Create detailed logging and analytics

---

## 📝 License

This project is open-source. Feel free to use, modify, and distribute.

---

## ⚠️ Disclaimer

This tool is designed to help identify potential scams, but should not be the sole basis for decision-making. Always:
- Verify company information independently
- Be cautious of unsolicited job offers
- Never pay upfront fees for job applications
- Check company websites and contact HR directly

---

## 🐛 Troubleshooting

### **Issue: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
pip install -r requirements.txt
```

### **Issue: "Address already in use" when starting server**
Change port:
```bash
python -m uvicorn api.main:app --port 8001
```

### **Issue: Company verification always returns "not found"**
The verifier now queries the public OpenCorporates registry API. If needed:
1. Set `COMPANY_REGISTRY_API_KEY` in `.env` (optional but recommended for higher limits)
2. Verify `COMPANY_REGISTRY_API_URL` is reachable from your environment
3. Restart the server

---

## 📞 Support

For issues or questions:
1. Check this README first
2. Review the API documentation at `/docs`
3. Check test cases in `test_detector.py`
4. Review code comments in `core/` modules

---

**Built with ❤️ to protect job seekers from fraud**
