Resume Optimizer AI

A smart, AI-powered resume optimizer built with **Streamlit** and **Mistral LLM API**. Upload your resume, paste a job description, and get instant feedback, tailored resumes, interview prep, and more.

Features

- Resume Analysis – Match resume with job description  
- Tailored Resume Generation – Rewrite your resume using job-specific keywords  
- Score Checker – See how well your resume fits the JD  
- Interview Readiness Analyzer – Get 5 technical and 5 behavioral questions with suggested answers


Tech Stack

- Python
- Streamlit
- Mistral LLM (via OpenAI wrapper)
- PyMuPDF – Resume text extraction from PDF
- ReportLab – Dynamic PDF generation



Setup & Run Locally

1. Clone the repository

```bash
git clone https://github.com/monit-jangir/resume-optimizer.git
cd resume-optimizer
````

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add your API key

Create `.streamlit/secrets.toml` and paste:

```toml
API_KEY = "your_mistral_api_key"
BASE_URL = "https://api.mistral.ai/v1"
```

5. Run the app

```bash
streamlit run app.py
```



Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo and deploy
4. In "Secrets", add:

```toml
API_KEY = "your_mistral_api_key"
BASE_URL = "https://api.mistral.ai/v1"
```

Contributing

PRs and ideas welcome. Let’s make resumes smarter.



License

MIT



Made by [@monit-jangir](https://github.com/monit-jangir)


