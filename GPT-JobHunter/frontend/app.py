"""
GPT-JobHunter Streamlit Frontend
AI-Powered Job Hunting Assistant UI
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any
import json
import os
from datetime import datetime, timedelta


# Page configuration
st.set_page_config(
    page_title="GPT-JobHunter",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
HEADERS = {"Content-Type": "application/json"}

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)


class JobHunterAPI:
    """API client for GPT-JobHunter backend."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {}
    
    def register_user(self, email: str, full_name: str, password: str) -> Dict[str, Any]:
        """Register new user."""
        data = {
            "email": email,
            "full_name": full_name,
            "password": password
        }
        return self._make_request("POST", "/auth/register", json=data, headers=HEADERS)
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user."""
        params = {"email": email, "password": password}
        return self._make_request("POST", "/auth/login", params=params, headers=HEADERS)
    
    def get_profile(self, token: str) -> Dict[str, Any]:
        """Get user profile."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("GET", "/profile", headers=headers)
    
    def update_profile(self, token: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("PUT", "/profile", json=profile_data, headers=headers)
    
    def search_jobs(self, token: str, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Search for jobs."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("POST", "/jobs/search", json=search_params, headers=headers)
    
    def get_job_recommendations(self, token: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get job recommendations."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        params = {"limit": limit}
        return self._make_request("GET", "/jobs/recommendations", params=params, headers=headers)
    
    def analyze_resume(self, token: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("POST", "/resume/analyze", json=analysis_data, headers=headers)
    
    def optimize_resume(self, token: str, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resume."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("POST", "/resume/optimize", json=optimization_data, headers=headers)
    
    def generate_cover_letter(self, token: str, cover_letter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cover letter."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("POST", "/cover-letter/generate", json=cover_letter_data, headers=headers)
    
    def prepare_interview(self, token: str, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare for interview."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("POST", "/interview/prepare", json=prep_data, headers=headers)
    
    def get_job_market_analysis(self, token: str, skills: List[str], location: str = None) -> List[Dict[str, Any]]:
        """Get job market analysis."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        params = {"skills": skills}
        if location:
            params["location"] = location
        return self._make_request("GET", "/analytics/job-market", params=params, headers=headers)
    
    def get_career_advice(self, token: str, advice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get career advice."""
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        return self._make_request("POST", "/analytics/career-advice", json=advice_data, headers=headers)


# Initialize API client
api = JobHunterAPI(API_BASE_URL)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_token" not in st.session_state:
    st.session_state.user_token = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None


def authenticate_user():
    """User authentication UI."""
    st.markdown('<h1 class="main-header">🚀 GPT-JobHunter</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-Powered Job Hunting Assistant")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button and email and password:
                result = api.login_user(email, password)
                if result and "access_token" in result:
                    st.session_state.authenticated = True
                    st.session_state.user_token = result["access_token"]
                    st.session_state.user_data = result.get("user", {})
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register", use_container_width=True)
            
            if register_button and all([full_name, email, password, confirm_password]):
                if password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                else:
                    result = api.register_user(email, full_name, password)
                    if result and "access_token" in result:
                        st.session_state.authenticated = True
                        st.session_state.user_token = result["access_token"]
                        st.session_state.user_data = result.get("user", {})
                        st.success("Registration successful!")
                        st.rerun()
                    else:
                        st.error("Registration failed. Please try again.")


def sidebar_navigation():
    """Sidebar navigation."""
    st.sidebar.title("🚀 GPT-JobHunter")
    st.sidebar.markdown(f"Welcome, **{st.session_state.user_data.get('full_name', 'User')}**!")
    
    pages = {
        "🏠 Dashboard": "dashboard",
        "👤 Profile": "profile",
        "🔍 Job Search": "job_search",
        "📋 Applications": "applications",
        "📄 Resume Tools": "resume_tools",
        "✉️ Cover Letters": "cover_letters",
        "🎯 Interview Prep": "interview_prep",
        "📊 Career Analytics": "analytics"
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_token = None
        st.session_state.user_data = None
        st.rerun()
    
    return pages[selected_page]


def dashboard_page():
    """Dashboard page."""
    st.title("📊 Dashboard")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Applications", "12", "2")
    
    with col2:
        st.metric("Interviews", "3", "1")
    
    with col3:
        st.metric("Profile Views", "45", "8")
    
    with col4:
        st.metric("Response Rate", "25%", "5%")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    # Sample data for chart
    dates = pd.date_range(start="2024-01-01", end="2024-01-31", freq="D")
    applications = [2, 1, 3, 0, 1, 2, 1, 0, 2, 3, 1, 2, 0, 1, 1, 2, 3, 1, 0, 2, 1, 1, 2, 0, 3, 1, 2, 1, 0, 2, 1]
    
    df = pd.DataFrame({"Date": dates, "Applications": applications[:len(dates)]})
    
    fig = px.line(df, x="Date", y="Applications", title="Job Applications Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Search Jobs", use_container_width=True):
            st.session_state.current_page = "job_search"
    
    with col2:
        if st.button("📄 Analyze Resume", use_container_width=True):
            st.session_state.current_page = "resume_tools"
    
    with col3:
        if st.button("✉️ Generate Cover Letter", use_container_width=True):
            st.session_state.current_page = "cover_letters"


def profile_page():
    """Profile management page."""
    st.title("👤 Profile Management")
    
    # Get current profile
    profile_data = api.get_profile(st.session_state.user_token)
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            headline = st.text_input("Professional Headline", 
                                   value=profile_data.get("headline", ""),
                                   placeholder="Senior Software Engineer")
            location = st.text_input("Location", 
                                   value=profile_data.get("location", ""),
                                   placeholder="San Francisco, CA")
            phone = st.text_input("Phone", 
                                value=profile_data.get("phone", ""),
                                placeholder="+1 (555) 123-4567")
            experience_level = st.selectbox("Experience Level",
                                          ["entry", "mid", "senior", "lead", "executive"],
                                          index=2 if not profile_data.get("experience_level") else 
                                          ["entry", "mid", "senior", "lead", "executive"].index(profile_data.get("experience_level")))
        
        with col2:
            linkedin_url = st.text_input("LinkedIn URL", 
                                       value=profile_data.get("linkedin_url", ""),
                                       placeholder="https://linkedin.com/in/yourprofile")
            github_url = st.text_input("GitHub URL", 
                                     value=profile_data.get("github_url", ""),
                                     placeholder="https://github.com/yourusername")
            portfolio_url = st.text_input("Portfolio URL", 
                                        value=profile_data.get("portfolio_url", ""),
                                        placeholder="https://yourportfolio.com")
            desired_salary_min = st.number_input("Desired Salary Min", 
                                               value=profile_data.get("desired_salary_min", 0),
                                               min_value=0, step=5000)
        
        summary = st.text_area("Professional Summary", 
                             value=profile_data.get("summary", ""),
                             placeholder="Experienced software engineer with expertise in...",
                             height=100)
        
        skills = st.text_input("Skills (comma-separated)", 
                             value=", ".join(profile_data.get("skills", [])),
                             placeholder="Python, JavaScript, React, FastAPI")
        
        if st.form_submit_button("Update Profile", use_container_width=True):
            update_data = {
                "headline": headline,
                "summary": summary,
                "location": location,
                "phone": phone,
                "linkedin_url": linkedin_url,
                "github_url": github_url,
                "portfolio_url": portfolio_url,
                "experience_level": experience_level,
                "desired_salary_min": desired_salary_min,
                "skills": [skill.strip() for skill in skills.split(",") if skill.strip()]
            }
            
            result = api.update_profile(st.session_state.user_token, update_data)
            if result:
                st.success("Profile updated successfully!")
            else:
                st.error("Failed to update profile.")


def job_search_page():
    """Job search page."""
    st.title("🔍 Job Search")
    
    # Search form
    with st.form("job_search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            query = st.text_input("Job Title or Keywords", placeholder="Python Developer")
            location = st.text_input("Location", placeholder="San Francisco, CA")
            job_type = st.selectbox("Job Type", ["", "full_time", "part_time", "contract", "internship", "freelance"])
        
        with col2:
            experience_level = st.selectbox("Experience Level", ["", "entry", "mid", "senior", "lead", "executive"])
            salary_min = st.number_input("Minimum Salary", min_value=0, step=5000)
            remote_only = st.checkbox("Remote Only")
        
        skills = st.text_input("Required Skills (comma-separated)", placeholder="Python, FastAPI, PostgreSQL")
        
        search_button = st.form_submit_button("Search Jobs", use_container_width=True)
    
    if search_button and query:
        search_params = {
            "query": query,
            "location": location,
            "job_type": job_type if job_type else None,
            "experience_level": experience_level if experience_level else None,
            "salary_min": salary_min if salary_min > 0 else None,
            "remote_only": remote_only,
            "skills": [skill.strip() for skill in skills.split(",") if skill.strip()],
            "page": 1,
            "limit": 20
        }
        
        results = api.search_jobs(st.session_state.user_token, search_params)
        
        if results and "jobs" in results:
            st.subheader(f"Found {results['total']} jobs")
            
            for job in results["jobs"]:
                with st.expander(f"{job['title']} at {job['company']} - Match: {job.get('match_score', 0):.1f}%"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Location:** {job.get('location', 'Not specified')}")
                        st.write(f"**Type:** {job.get('job_type', 'Not specified').replace('_', ' ').title()}")
                        st.write(f"**Experience:** {job.get('experience_level', 'Not specified').title()}")
                        if job.get('salary_min') and job.get('salary_max'):
                            st.write(f"**Salary:** ${job['salary_min']:,} - ${job['salary_max']:,}")
                        st.write("**Description:**")
                        st.write(job['description'][:200] + "..." if len(job['description']) > 200 else job['description'])
                    
                    with col2:
                        st.metric("Match Score", f"{job.get('match_score', 0):.1f}%")
                        if st.button(f"Apply", key=f"apply_{job['id']}"):
                            st.success("Application tracked!")
        else:
            st.info("No jobs found. Try adjusting your search criteria.")
    
    # Job recommendations
    st.subheader("💡 Recommended Jobs")
    recommendations = api.get_job_recommendations(st.session_state.user_token, limit=5)
    
    if recommendations:
        for job in recommendations:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{job['title']}** at {job['company']}")
                    st.write(f"📍 {job.get('location', 'Remote')}")
                
                with col2:
                    st.metric("Match", f"{job.get('match_score', 0):.1f}%")
                
                with col3:
                    if st.button("View Details", key=f"view_{job['id']}"):
                        st.info("Job details would open here")


def resume_tools_page():
    """Resume tools page."""
    st.title("📄 Resume Tools")
    
    tab1, tab2 = st.tabs(["Analyze Resume", "Optimize Resume"])
    
    with tab1:
        st.subheader("📊 Resume Analysis")
        
        analysis_method = st.radio("Analysis Method", ["Paste Text", "Upload File"])
        
        if analysis_method == "Paste Text":
            resume_text = st.text_area("Paste your resume text here:", height=200)
            
            if st.button("Analyze Resume", use_container_width=True) and resume_text:
                analysis_data = {
                    "text_content": resume_text,
                    "target_job_description": None
                }
                
                result = api.analyze_resume(st.session_state.user_token, analysis_data)
                
                if result:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("ATS Score", f"{result['ats_score']:.1f}/100")
                    
                    with col2:
                        st.metric("Keyword Match", f"{result['keyword_match']:.1f}/100")
                    
                    with col3:
                        st.metric("Overall Score", f"{result['overall_score']:.1f}/100")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("✅ Strengths")
                        for strength in result['strengths']:
                            st.write(f"• {strength}")
                        
                        st.subheader("💡 Suggestions")
                        for suggestion in result['suggestions']:
                            st.write(f"• {suggestion}")
                    
                    with col2:
                        st.subheader("⚠️ Areas for Improvement")
                        for weakness in result['weaknesses']:
                            st.write(f"• {weakness}")
                        
                        st.subheader("🎯 Missing Skills")
                        for skill in result['missing_skills']:
                            st.write(f"• {skill}")
        
        else:
            uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'])
            
            if uploaded_file and st.button("Analyze Resume", use_container_width=True):
                st.info("File upload analysis would be implemented here")
    
    with tab2:
        st.subheader("🚀 Resume Optimization")
        
        current_resume = st.text_area("Current Resume Text:", height=200)
        target_job = st.text_area("Target Job Description:", height=150)
        
        if st.button("Optimize Resume", use_container_width=True) and current_resume and target_job:
            optimization_data = {
                "current_resume": current_resume,
                "target_job_description": target_job,
                "focus_areas": []
            }
            
            result = api.optimize_resume(st.session_state.user_token, optimization_data)
            
            if result:
                st.subheader("✨ Optimized Resume")
                st.text_area("", value=result['optimized_resume'], height=300)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔄 Changes Made")
                    for change in result['changes_made']:
                        st.write(f"• {change}")
                
                with col2:
                    st.subheader("📈 Improvement Areas")
                    for area in result['improvement_areas']:
                        st.write(f"• {area}")


def cover_letters_page():
    """Cover letter generation page."""
    st.title("✉️ Cover Letter Generator")
    
    with st.form("cover_letter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="TechCorp Inc.")
            position_title = st.text_input("Position Title", placeholder="Senior Software Engineer")
            tone = st.selectbox("Tone", ["professional", "casual", "enthusiastic", "formal"])
        
        with col2:
            length = st.selectbox("Length", ["short", "medium", "long"])
            user_background = st.text_area("Your Background (optional)", 
                                         placeholder="Brief summary of your relevant experience...",
                                         height=80)
        
        job_description = st.text_area("Job Description", 
                                     placeholder="Paste the job description here...",
                                     height=150)
        
        generate_button = st.form_submit_button("Generate Cover Letter", use_container_width=True)
    
    if generate_button and all([company_name, position_title, job_description]):
        cover_letter_data = {
            "job_description": job_description,
            "company_name": company_name,
            "position_title": position_title,
            "user_background": user_background,
            "tone": tone,
            "length": length
        }
        
        result = api.generate_cover_letter(st.session_state.user_token, cover_letter_data)
        
        if result:
            st.subheader("📝 Generated Cover Letter")
            st.text_area("", value=result['cover_letter'], height=400)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Key Points Highlighted")
                for point in result['key_points_highlighted']:
                    st.write(f"• {point}")
            
            with col2:
                st.subheader("💡 Suggestions")
                for suggestion in result['suggestions']:
                    st.write(f"• {suggestion}")


def interview_prep_page():
    """Interview preparation page."""
    st.title("🎯 Interview Preparation")
    
    with st.form("interview_prep_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="TechCorp Inc.")
            position_title = st.text_input("Position Title", placeholder="Senior Software Engineer")
        
        with col2:
            interview_type = st.selectbox("Interview Type", ["general", "technical", "behavioral", "case_study"])
            experience_level = st.selectbox("Experience Level", ["entry", "mid", "senior", "lead", "executive"])
        
        job_description = st.text_area("Job Description", 
                                     placeholder="Paste the job description here...",
                                     height=150)
        
        prepare_button = st.form_submit_button("Generate Interview Prep", use_container_width=True)
    
    if prepare_button and all([company_name, position_title, job_description]):
        prep_data = {
            "job_description": job_description,
            "company_name": company_name,
            "position_title": position_title,
            "interview_type": interview_type,
            "experience_level": experience_level
        }
        
        result = api.prepare_interview(st.session_state.user_token, prep_data)
        
        if result:
            # Interview questions
            st.subheader("❓ Interview Questions")
            
            for i, question in enumerate(result['questions'], 1):
                with st.expander(f"Question {i}: {question['question']} ({question['difficulty'].title()})"):
                    st.write(f"**Category:** {question['category'].title()}")
                    st.write(f"**Suggested Answer:** {question['suggested_answer']}")
                    st.write("**Tips:**")
                    for tip in question['tips']:
                        st.write(f"• {tip}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏢 Company Insights")
                for insight in result['company_insights']:
                    st.write(f"• {insight}")
                
                st.subheader("📚 Preparation Tips")
                for tip in result['preparation_tips']:
                    st.write(f"• {tip}")
            
            with col2:
                st.subheader("🔍 Research Suggestions")
                for suggestion in result['research_suggestions']:
                    st.write(f"• {suggestion}")


def analytics_page():
    """Career analytics page."""
    st.title("📊 Career Analytics")
    
    tab1, tab2 = st.tabs(["Job Market Analysis", "Career Advice"])
    
    with tab1:
        st.subheader("📈 Job Market Analysis")
        
        skills_input = st.text_input("Skills to analyze (comma-separated)", 
                                   placeholder="Python, JavaScript, React")
        location_input = st.text_input("Location (optional)", placeholder="San Francisco, CA")
        
        if st.button("Analyze Market", use_container_width=True) and skills_input:
            skills = [skill.strip() for skill in skills_input.split(",")]
            analysis = api.get_job_market_analysis(st.session_state.user_token, skills, location_input)
            
            if analysis:
                for skill_analysis in analysis:
                    st.subheader(f"📊 {skill_analysis['skill']}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Demand Score", f"{skill_analysis['demand_score']:.1f}/100")
                    
                    with col2:
                        if skill_analysis.get('average_salary'):
                            st.metric("Average Salary", f"${skill_analysis['average_salary']:,}")
                    
                    with col3:
                        trend_emoji = "📈" if skill_analysis['growth_trend'] == "increasing" else "📉" if skill_analysis['growth_trend'] == "decreasing" else "➡️"
                        st.metric("Growth Trend", f"{trend_emoji} {skill_analysis['growth_trend'].title()}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Top Companies:**")
                        for company in skill_analysis['top_companies']:
                            st.write(f"• {company}")
                    
                    with col2:
                        st.write("**Related Skills:**")
                        for related_skill in skill_analysis['related_skills']:
                            st.write(f"• {related_skill}")
    
    with tab2:
        st.subheader("🎯 Career Advancement Advice")
        
        with st.form("career_advice_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                current_role = st.text_input("Current Role", placeholder="Software Engineer")
                target_role = st.text_input("Target Role", placeholder="Senior Software Engineer")
                experience_years = st.number_input("Years of Experience", min_value=0, max_value=50, value=3)
            
            with col2:
                skills = st.text_input("Current Skills (comma-separated)", 
                                     placeholder="Python, JavaScript, React")
                industry = st.text_input("Industry (optional)", placeholder="Technology")
            
            advice_button = st.form_submit_button("Get Career Advice", use_container_width=True)
        
        if advice_button and all([current_role, target_role, skills]):
            advice_data = {
                "current_role": current_role,
                "target_role": target_role,
                "experience_years": experience_years,
                "skills": [skill.strip() for skill in skills.split(",")],
                "industry": industry
            }
            
            result = api.get_career_advice(st.session_state.user_token, advice_data)
            
            if result:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Skill Gaps")
                    for gap in result['skill_gaps']:
                        st.write(f"• {gap}")
                    
                    st.subheader("📚 Learning Path")
                    for i, step in enumerate(result['learning_path'], 1):
                        st.write(f"{i}. {step}")
                    
                    st.subheader("🏆 Recommended Certifications")
                    for cert in result['recommended_certifications']:
                        st.write(f"• {cert}")
                
                with col2:
                    st.subheader("💰 Salary Expectations")
                    for key, value in result['salary_expectations'].items():
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                    
                    st.subheader("🤝 Networking Tips")
                    for tip in result['networking_tips']:
                        st.write(f"• {tip}")
                    
                    st.metric("Timeline", f"{result['timeline_months']} months")


def applications_page():
    """Job applications tracking page."""
    st.title("📋 Application Tracking")
    
    # This would typically fetch real application data
    st.info("Application tracking functionality would display your job applications here with status updates, follow-up reminders, and analytics.")
    
    # Sample application data for demonstration
    sample_applications = [
        {"company": "TechCorp", "position": "Senior Developer", "status": "Applied", "date": "2024-01-15"},
        {"company": "StartupXYZ", "position": "Full Stack Engineer", "status": "Interviewing", "date": "2024-01-10"},
        {"company": "MegaCorp", "position": "Lead Architect", "status": "Offered", "date": "2024-01-05"},
    ]
    
    df = pd.DataFrame(sample_applications)
    st.dataframe(df, use_container_width=True)


def main():
    """Main application."""
    if not st.session_state.authenticated:
        authenticate_user()
    else:
        # Sidebar navigation
        current_page = sidebar_navigation()
        
        # Page routing
        if current_page == "dashboard":
            dashboard_page()
        elif current_page == "profile":
            profile_page()
        elif current_page == "job_search":
            job_search_page()
        elif current_page == "applications":
            applications_page()
        elif current_page == "resume_tools":
            resume_tools_page()
        elif current_page == "cover_letters":
            cover_letters_page()
        elif current_page == "interview_prep":
            interview_prep_page()
        elif current_page == "analytics":
            analytics_page()


if __name__ == "__main__":
    main()