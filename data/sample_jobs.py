"""Sample test cases for the detector."""
from core.schemas import JobPost


# Example FAKE job posting
FAKE_JOB_1 = JobPost(
    title="Data Analyst",
    company_name="Tech Solutions Inc",
    description="""
    GUARANTEED JOB!!! 🎉🎊
    
    NO INTERVIEW NEEDED!
    
    Earn ₹80,000/month from home with NO EXPERIENCE REQUIRED!!!
    
    Pay a ONE-TIME REGISTRATION FEE of ₹5,000 and get hired immediately.
    Limited seats available - APPLY NOW before it closes!
    
    Must provide bank account details and Aadhar number for processing.
    """,
    salary_min=80_000,
    salary_max=80_000,
    currency="INR",
    experience_required="Fresher",
    job_type="Full-time",
    platform="LinkedIn",
    location="Work from home",
)

# Example FAKE job posting 2
FAKE_JOB_2 = JobPost(
    title="Software Engineer",
    company_name="Unknown Startup XYZ",
    description="Urgent hiring for Software Engineers. No tests. Direct hiring. Easy process.",
    salary_min=500_000,
    salary_max=500_000,
    currency="INR",
    experience_required="0-2 years",
    company_website=None,
    platform="Indeed",
    location="Remote",
)

# Example SUSPICIOUS job posting
SUSPICIOUS_JOB_1 = JobPost(
    title="Business Analyst",
    company_name="XYZ Consultancy",
    description="""
    We are looking for a Business Analyst with 5-7 years of experience.
    
    Responsibilities:
    - Analyze business processes
    - Create technical specifications
    - Work with cross-functional teams
    
    This is an urgent requirement. Please apply immediately.
    """,
    salary_min=1_500_000,
    salary_max=2_500_000,
    currency="INR",
    experience_required="5-7 years",
    job_type="Full-time",
    platform="LinkedIn",
    location="Bangalore",
)

# Example LEGITIMATE job posting
LEGITIMATE_JOB_1 = JobPost(
    title="Senior Software Engineer",
    company_name="Google",
    description="""
    Google is looking for a Senior Software Engineer to join our Cloud team.
    
    Responsibilities:
    - Design and build scalable systems
    - Mentor junior engineers
    - Contribute to open source
    - Collaborate with product teams
    
    Requirements:
    - 5+ years of software development experience
    - Strong knowledge of distributed systems
    - Experience with cloud platforms (GCP, AWS, or Azure)
    - Bachelor's degree in Computer Science or related field
    
    We offer competitive compensation, comprehensive benefits, and a collaborative culture.
    """,
    salary_min=2_500_000,
    salary_max=3_500_000,
    currency="INR",
    experience_required="5+ years",
    job_type="Full-time",
    platform="Google Careers",
    company_website="https://www.google.com",
    location="Bangalore, India",
)

# Example LEGITIMATE job posting 2
LEGITIMATE_JOB_2 = JobPost(
    title="Data Scientist",
    company_name="Microsoft",
    description="""
    Microsoft is hiring Data Scientists for our AI and Research division.
    
    About the role:
    - Develop machine learning models for production systems
    - Work with large-scale datasets
    - Collaborate with researchers and engineers
    - Publish research papers and present findings
    
    Qualifications:
    - Master's or PhD in Computer Science, Statistics, Mathematics, or related field
    - 3+ years of experience in data science or machine learning
    - Strong programming skills in Python or R
    - Experience with ML frameworks (TensorFlow, PyTorch, scikit-learn)
    
    We provide competitive salary, stock options, health insurance, and tuition reimbursement.
    """,
    salary_min=2_000_000,
    salary_max=3_000_000,
    currency="INR",
    experience_required="3-5 years",
    job_type="Full-time",
    platform="Microsoft Careers",
    company_website="https://www.microsoft.com",
    location="Hyderabad, India",
)


if __name__ == "__main__":
    print("Sample test jobs defined. Use these in tests.")
