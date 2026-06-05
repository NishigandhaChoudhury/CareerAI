# 🚀 CareerAI – Smart Internship & Job Matcher

AI-powered platform that matches students to internships/jobs based on skills, projects, and GitHub — not just resumes.

## Features
- **Profile Analysis** — skills, projects, education, GitHub
- **Smart Matching** — 5 personalized job/internship matches with match scores
- **Success Prediction** — probability of succeeding in each role
- **Gap Analysis** — skills to build, action tips per role
- **Career Roadmap** — AI-generated 1-year path

## Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/smart-internship-matcher
cd smart-internship-matcher
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

```bash
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set main file as `app.py`
4. Under **Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click **Deploy** ✅

## Tech Stack
- **Frontend**: Streamlit
- **AI**: Anthropic Claude (claude-sonnet-4)
- **Language**: Python
