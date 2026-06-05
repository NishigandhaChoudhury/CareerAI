import streamlit as st
import anthropic
import json
import re

st.set_page_config(
    page_title="CareerAI – Smart Job Matcher",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }
code, .mono { font-family: 'JetBrains Mono', monospace; }

.stApp { background: #0a0a0f; color: #e8e8f0; }

.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0d1a2e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(100,60,255,0.12) 0%, transparent 60%);
    pointer-events: none;
}
.hero h1 { font-size: 2.8rem; font-weight: 700; margin: 0; 
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: #8888aa; font-size: 1.1rem; margin-top: 0.5rem; }

.match-card {
    background: #12121e;
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.match-card:hover { border-color: #7c3aed; }

.score-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}
.score-high { background: rgba(52,211,153,0.2); color: #34d399; border: 1px solid #34d399; }
.score-mid  { background: rgba(251,191,36,0.2);  color: #fbbf24; border: 1px solid #fbbf24; }
.score-low  { background: rgba(248,113,113,0.2); color: #f87171; border: 1px solid #f87171; }

.tag {
    display: inline-block;
    background: rgba(124,58,237,0.2);
    color: #a78bfa;
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.78rem;
    margin: 0.2rem;
}
.section-label { color: #6666aa; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem; }
.insight-box {
    background: rgba(96,165,250,0.07);
    border-left: 3px solid #60a5fa;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.95rem;
    color: #c8d8f0;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #12121e !important;
    border: 1px solid #2a2a3e !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>🚀 CareerAI</h1>
    <p>AI-powered internship & job matching — beyond your resume</p>
</div>
""", unsafe_allow_html=True)

# Sidebar – Profile Input
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
    
    skills = st.text_area("Skills (comma-separated)", 
        placeholder="Python, ML, React, SQL...", height=80)
    
    projects = st.text_area("Projects / Work Done", 
        placeholder="Built a sentiment analysis tool using BERT, deployed on Flask...", height=100)
    
    github = st.text_input("GitHub URL (optional)", placeholder="https://github.com/username")
    
    education = st.text_input("Education", placeholder="B.Tech CSE, 3rd Year, Alliance University")
    
    role_pref = st.selectbox("Looking For", 
        ["Internship", "Full-time Job", "Both"])
    
    domain_pref = st.multiselect("Preferred Domains",
        ["Data Science / ML", "Web Development", "Backend Engineering",
         "DevOps / Cloud", "Mobile Dev", "Cybersecurity", "Product Management"],
        default=["Data Science / ML"])
    
    analyze_btn = st.button("🔍 Find My Matches")

# Main content
if analyze_btn:
    if not skills or not projects:
        st.warning("Please fill in at least Skills and Projects.")
    else:
        with st.spinner("Analyzing your profile with AI..."):
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            
            profile = {
                "name": name or "Student",
                "skills": skills,
                "projects": projects,
                "github": github,
                "education": education,
                "looking_for": role_pref,
                "preferred_domains": domain_pref
            }
            
            prompt = f"""You are an AI career counselor. Analyze this student profile and return ONLY valid JSON.

Profile:
{json.dumps(profile, indent=2)}

Return this exact JSON structure (no markdown, no extra text):
{{
  "profile_summary": "2-sentence summary of the student's strengths",
  "skill_gaps": ["gap1", "gap2", "gap3"],
  "matches": [
    {{
      "title": "Job/Internship Title",
      "company_type": "Type of company (startup/MNC/research lab)",
      "domain": "Domain",
      "match_score": 85,
      "why_matched": "Specific reason based on their projects/skills",
      "required_skills": ["skill1", "skill2"],
      "missing_skills": ["skill1"],
      "success_probability": 78,
      "success_reason": "Why they'd succeed or struggle",
      "action_tip": "One specific action to improve chances"
    }}
  ],
  "top_strength": "Their single biggest strength",
  "career_path": "Suggested 1-year career roadmap in 2 sentences"
}}

Generate 5 diverse matches. Match scores and success probabilities must be realistic integers 40-95."""

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            raw = response.content[0].text.strip()
            # Strip markdown fences if present
            raw = re.sub(r"^```json\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()
            
            try:
                data = json.loads(raw)
            except:
                st.error("Parsing error. Raw response:")
                st.code(raw)
                st.stop()
        
        # Results
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("## 🎯 Your Top Matches")
            
            for i, match in enumerate(data.get("matches", [])):
                score = match.get("match_score", 0)
                if score >= 75:
                    badge_cls = "score-high"
                elif score >= 55:
                    badge_cls = "score-mid"
                else:
                    badge_cls = "score-low"
                
                succ = match.get("success_probability", 0)
                
                skills_html = "".join(f'<span class="tag">{s}</span>' for s in match.get("required_skills", []))
                missing_html = "".join(f'<span class="tag" style="background:rgba(248,113,113,0.1);color:#f87171;border-color:rgba(248,113,113,0.4)">{s}</span>' for s in match.get("missing_skills", []))
                
                st.markdown(f"""
<div class="match-card">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
        <div>
            <span style="font-size:1.15rem; font-weight:600; color:#e8e8f0">{match.get('title','')}</span>
            <span style="color:#6666aa; margin-left:0.5rem; font-size:0.9rem">· {match.get('company_type','')}</span>
        </div>
        <span class="score-badge {badge_cls}">Match: {score}%</span>
    </div>
    <div style="color:#a78bfa; font-size:0.85rem; margin:0.4rem 0;">{match.get('domain','')}</div>
    
    <div class="insight-box">{match.get('why_matched','')}</div>
    
    <div style="margin-top:0.8rem;">
        <div class="section-label">Required Skills</div>
        {skills_html}
    </div>
    {"<div style='margin-top:0.5rem;'><div class='section-label'>Skills to Build</div>" + missing_html + "</div>" if match.get('missing_skills') else ""}
    
    <div style="margin-top:0.8rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
        <div>
            <span class="section-label">Success Probability</span>
            <div style="font-size:1.1rem; font-weight:600; color:{'#34d399' if succ>=70 else '#fbbf24' if succ>=50 else '#f87171'}">{succ}%</div>
        </div>
        <div style="max-width:60%; text-align:right; color:#8888aa; font-size:0.85rem">{match.get('success_reason','')}</div>
    </div>
    
    <div style="margin-top:0.8rem; background:rgba(52,211,153,0.07); border-radius:6px; padding:0.6rem 0.8rem; font-size:0.88rem; color:#6ee7b7;">
        💡 {match.get('action_tip','')}
    </div>
</div>
""", unsafe_allow_html=True)

        with col2:
            st.markdown("## 📊 Profile Insights")
            
            st.markdown(f"""
<div class="match-card">
    <div class="section-label">Profile Summary</div>
    <p style="color:#c8c8e8; margin:0.5rem 0 0">{data.get('profile_summary','')}</p>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="match-card">
    <div class="section-label">⭐ Top Strength</div>
    <p style="color:#34d399; font-weight:600; margin:0.5rem 0 0">{data.get('top_strength','')}</p>
</div>
""", unsafe_allow_html=True)

            if data.get("skill_gaps"):
                gaps_html = "".join(f'<span class="tag" style="background:rgba(251,191,36,0.1);color:#fbbf24;border-color:rgba(251,191,36,0.4)">{g}</span>' for g in data["skill_gaps"])
                st.markdown(f"""
<div class="match-card">
    <div class="section-label">🔧 Skill Gaps to Address</div>
    <div style="margin-top:0.5rem">{gaps_html}</div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="match-card">
    <div class="section-label">🗺️ Career Roadmap</div>
    <p style="color:#c8c8e8; margin:0.5rem 0 0; line-height:1.6">{data.get('career_path','')}</p>
</div>
""", unsafe_allow_html=True)

else:
    # Landing state
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "🧠", "Beyond Resumes", "Analyzes projects, GitHub & skills — not just your CV"),
        (c2, "🎯", "Smart Matching", "AI matches you with roles where you'll actually succeed"),
        (c3, "📈", "Success Prediction", "Know your probability of landing & thriving in each role"),
    ]:
        with col:
            st.markdown(f"""
<div class="match-card" style="text-align:center; padding:2rem 1.5rem;">
    <div style="font-size:2.2rem">{icon}</div>
    <div style="font-size:1.1rem; font-weight:600; margin:0.8rem 0 0.4rem; color:#e8e8f0">{title}</div>
    <div style="color:#6666aa; font-size:0.9rem">{desc}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div style="text-align:center; color:#6666aa; margin-top:2rem; font-size:0.95rem">
    ← Fill in your profile and click <strong style="color:#a78bfa">Find My Matches</strong> to get started
</div>
""", unsafe_allow_html=True)
