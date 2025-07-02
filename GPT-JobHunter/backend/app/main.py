"""
GPT-JobHunter FastAPI Application
AI-Powered Job Hunting Assistant Backend
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import List, Optional, Dict, Any

from app.config import settings
from app.models.schemas import (
    # User and Auth schemas
    User, UserCreate, UserUpdate, Token,
    # Profile schemas
    Profile, ProfileCreate, ProfileUpdate,
    # Job schemas
    Job, JobCreate, JobSearchRequest, JobSearchResponse,
    # Application schemas
    Application, ApplicationCreate, ApplicationUpdate,
    # AI-powered feature schemas
    ResumeAnalysisRequest, ResumeAnalysisResponse,
    ResumeOptimizationRequest, ResumeOptimizationResponse,
    CoverLetterRequest, CoverLetterResponse,
    InterviewPrepRequest, InterviewPrepResponse,
    JobMarketAnalysis, CareerAdviceRequest, CareerAdviceResponse,
    # Utility schemas
    FileUploadResponse, SuccessResponse, ErrorResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting GPT-JobHunter API")
    yield
    # Shutdown
    logger.info("Shutting down GPT-JobHunter API")


# Create FastAPI app with comprehensive metadata
app = FastAPI(
    title=settings.api_title,
    description="""
    ## 🚀 GPT-JobHunter API

    An AI-powered job hunting assistant that helps you optimize your job search with cutting-edge technology.

    ### 🌟 Key Features

    * **Smart Job Search**: AI-powered job matching and recommendations
    * **Resume Analysis**: Advanced ATS-friendly resume optimization
    * **Cover Letter Generation**: Personalized cover letters for each application
    * **Interview Preparation**: Tailored interview questions and preparation tips
    * **Application Tracking**: Comprehensive job application management
    * **Career Insights**: Market analysis and career advancement recommendations

    ### 🔒 Authentication

    This API uses JWT (JSON Web Token) authentication. To access protected endpoints:

    1. Create an account using `/auth/register`
    2. Login using `/auth/login` to get your access token
    3. Include the token in the Authorization header: `Bearer <your_token>`

    ### 📊 API Workflow

    ```
    1. Register/Login → Get Access Token
    2. Create/Update Profile → Set up your professional profile
    3. Upload Resume → Analyze and optimize your resume
    4. Search Jobs → Find relevant opportunities
    5. Generate Materials → Create cover letters and prep for interviews
    6. Track Applications → Monitor your job search progress
    ```

    ### 🛠️ Rate Limits

    - **Free Tier**: 100 requests/hour
    - **Premium Tier**: 1000 requests/hour
    
    ### 📧 Support

    For API support, contact: support@gpt-jobhunter.com
    """,
    version=settings.api_version,
    contact={
        "name": "GPT-JobHunter Support",
        "url": "https://gpt-jobhunter.com/support",
        "email": "support@gpt-jobhunter.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.gpt-jobhunter.com",
            "description": "Production server"
        }
    ],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


# Dependency for getting current user (mock implementation)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user."""
    # This is a mock implementation - in real app, verify JWT token
    return User(
        id=1,
        email="user@example.com",
        full_name="John Doe",
        is_active=True
    )


# Root endpoint
@app.get(
    "/",
    summary="Root endpoint",
    description="Welcome message and API information",
    response_model=Dict[str, Any],
    tags=["System"]
)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to GPT-JobHunter API! 🚀",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "operational"
    }


# Health check endpoint
@app.get(
    "/health",
    summary="Health check",
    description="Check API health status",
    response_model=Dict[str, str],
    tags=["System"]
)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.api_version}


# === AUTHENTICATION ENDPOINTS ===

@app.post(
    "/auth/register",
    summary="Register new user",
    description="""
    Register a new user account.
    
    **Requirements:**
    - Valid email address
    - Password minimum 8 characters
    - Unique email (not already registered)
    
    **Returns:** User information and access token
    """,
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already registered"}
    }
)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    # Mock implementation
    user = User(
        id=1,
        email=user_data.email,
        full_name=user_data.full_name,
        is_active=True
    )
    
    return Token(
        access_token="mock_jwt_token_12345",
        token_type="bearer",
        expires_in=1800,
        user=user
    )


@app.post(
    "/auth/login",
    summary="User login",
    description="""
    Authenticate user and get access token.
    
    **Process:**
    1. Validate email and password
    2. Generate JWT access token
    3. Return token with user information
    
    **Token Usage:** Include in Authorization header as `Bearer <token>`
    """,
    response_model=Token,
    tags=["Authentication"],
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        404: {"description": "User not found"}
    }
)
async def login_user(email: str, password: str):
    """User login."""
    # Mock implementation
    user = User(
        id=1,
        email=email,
        full_name="John Doe",
        is_active=True
    )
    
    return Token(
        access_token="mock_jwt_token_12345",
        token_type="bearer",
        expires_in=1800,
        user=user
    )


# === PROFILE MANAGEMENT ===

@app.get(
    "/profile",
    summary="Get user profile",
    description="Retrieve the authenticated user's profile information",
    response_model=Profile,
    tags=["Profile Management"]
)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get user profile."""
    return Profile(
        id=1,
        user_id=current_user.id,
        headline="Senior Software Engineer",
        summary="Experienced developer with 5+ years in full-stack development",
        location="San Francisco, CA",
        skills=["Python", "JavaScript", "React", "FastAPI"],
        experience_level="senior"
    )


@app.post(
    "/profile",
    summary="Create user profile",
    description="""
    Create a new profile for the authenticated user.
    
    **Profile Features:**
    - Professional headline and summary
    - Contact information and social links
    - Skills and experience level
    - Salary expectations and preferences
    """,
    response_model=Profile,
    status_code=status.HTTP_201_CREATED,
    tags=["Profile Management"]
)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user)
):
    """Create user profile."""
    return Profile(
        id=1,
        user_id=current_user.id,
        **profile_data.dict()
    )


@app.put(
    "/profile",
    summary="Update user profile",
    description="Update the authenticated user's profile information",
    response_model=Profile,
    tags=["Profile Management"]
)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user profile."""
    return Profile(
        id=1,
        user_id=current_user.id,
        **profile_data.dict(exclude_unset=True)
    )


# === JOB SEARCH AND RECOMMENDATIONS ===

@app.post(
    "/jobs/search",
    summary="Search for jobs",
    description="""
    Search for jobs with AI-powered matching and recommendations.
    
    **Search Features:**
    - Keyword-based search with intelligent matching
    - Location and remote work filtering
    - Salary range and experience level filters
    - Skills-based recommendations
    - Personalized match scoring
    
    **AI Enhancements:**
    - Semantic search understanding
    - Profile-based job scoring
    - Hidden gem discovery
    """,
    response_model=JobSearchResponse,
    tags=["Job Search"]
)
async def search_jobs(
    search_request: JobSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search for jobs with AI recommendations."""
    # Mock implementation with sample jobs
    sample_jobs = [
        Job(
            id=1,
            title="Senior Python Developer",
            company="TechCorp Inc.",
            description="Looking for an experienced Python developer...",
            location="San Francisco, CA",
            salary_min=120000,
            salary_max=180000,
            job_type="full_time",
            experience_level="senior",
            remote_allowed=True,
            skills_required=["Python", "FastAPI", "PostgreSQL"],
            match_score=95.5
        ),
        Job(
            id=2,
            title="Full Stack Engineer",
            company="StartupXYZ",
            description="Join our dynamic team building the future...",
            location="Remote",
            salary_min=100000,
            salary_max=150000,
            job_type="full_time",
            experience_level="mid",
            remote_allowed=True,
            skills_required=["JavaScript", "React", "Node.js"],
            match_score=87.2
        )
    ]
    
    return JobSearchResponse(
        jobs=sample_jobs[:search_request.limit],
        total=len(sample_jobs),
        page=search_request.page,
        limit=search_request.limit,
        has_more=False
    )


@app.get(
    "/jobs/recommendations",
    summary="Get job recommendations",
    description="""
    Get personalized job recommendations based on your profile.
    
    **Recommendation Algorithm:**
    - Analyzes your skills and experience
    - Considers location and salary preferences
    - Identifies career growth opportunities
    - Finds jobs matching your interests
    """,
    response_model=List[Job],
    tags=["Job Search"]
)
async def get_job_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Get personalized job recommendations."""
    # Mock recommendations
    return [
        Job(
            id=3,
            title="Lead Software Architect",
            company="MegaCorp",
            description="Lead our architecture team...",
            location="Seattle, WA",
            salary_min=150000,
            salary_max=220000,
            job_type="full_time",
            experience_level="lead",
            remote_allowed=True,
            skills_required=["Python", "Architecture", "Leadership"],
            match_score=92.8
        )
    ]


# === APPLICATION TRACKING ===

@app.get(
    "/applications",
    summary="Get job applications",
    description="Retrieve all job applications for the authenticated user",
    response_model=List[Application],
    tags=["Application Tracking"]
)
async def get_applications(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get user's job applications."""
    # Mock implementation
    return []


@app.post(
    "/applications",
    summary="Create job application",
    description="""
    Create a new job application entry.
    
    **Application Features:**
    - Link to job posting
    - Track application status
    - Store cover letter and resume versions
    - Set follow-up reminders
    - Add personal notes
    """,
    response_model=Application,
    status_code=status.HTTP_201_CREATED,
    tags=["Application Tracking"]
)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new job application."""
    # Mock implementation
    job = Job(
        id=application_data.job_id,
        title="Sample Job",
        company="Sample Company",
        description="Sample description"
    )
    
    return Application(
        id=1,
        user_id=current_user.id,
        job=job,
        **application_data.dict()
    )


# === AI-POWERED RESUME SERVICES ===

@app.post(
    "/resume/analyze",
    summary="Analyze resume",
    description="""
    AI-powered resume analysis and ATS compatibility check.
    
    **Analysis Features:**
    - ATS (Applicant Tracking System) compatibility score
    - Keyword optimization suggestions
    - Structure and formatting recommendations
    - Content strength assessment
    - Missing skills identification
    
    **Input Options:**
    - Upload resume file (PDF, DOCX)
    - Paste resume text directly
    - Compare against specific job description
    """,
    response_model=ResumeAnalysisResponse,
    tags=["AI Resume Services"]
)
async def analyze_resume(
    analysis_request: ResumeAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze resume with AI-powered insights."""
    return ResumeAnalysisResponse(
        strengths=[
            "Strong technical skills section",
            "Quantified achievements with metrics",
            "Clear career progression"
        ],
        weaknesses=[
            "Missing industry-specific keywords",
            "Could improve summary section",
            "Limited use of action verbs"
        ],
        missing_skills=[
            "Docker", "Kubernetes", "AWS"
        ],
        suggestions=[
            "Add more specific technical achievements",
            "Include relevant certifications",
            "Optimize for ATS with better keyword usage"
        ],
        ats_score=78.5,
        keyword_match=65.2,
        overall_score=82.3
    )


@app.post(
    "/resume/optimize",
    summary="Optimize resume",
    description="""
    AI-powered resume optimization for specific job applications.
    
    **Optimization Features:**
    - ATS keyword integration
    - Content restructuring for impact
    - Industry-specific terminology
    - Achievement highlighting
    - Format optimization
    
    **Customization:**
    - Target specific job descriptions
    - Focus on particular skills/experiences
    - Maintain your personal style
    """,
    response_model=ResumeOptimizationResponse,
    tags=["AI Resume Services"]
)
async def optimize_resume(
    optimization_request: ResumeOptimizationRequest,
    current_user: User = Depends(get_current_user)
):
    """Optimize resume for specific job application."""
    return ResumeOptimizationResponse(
        optimized_resume="Your optimized resume content here...",
        changes_made=[
            "Added relevant keywords from job description",
            "Restructured experience section for better flow",
            "Enhanced technical skills section",
            "Improved action verb usage"
        ],
        improvement_areas=[
            "Consider adding more quantified achievements",
            "Include relevant industry certifications",
            "Expand on leadership experiences"
        ]
    )


# === AI-POWERED COVER LETTER SERVICES ===

@app.post(
    "/cover-letter/generate",
    summary="Generate cover letter",
    description="""
    AI-powered personalized cover letter generation.
    
    **Generation Features:**
    - Company and role-specific content
    - Personal background integration
    - Industry-appropriate tone and style
    - Keyword optimization
    - Multiple length options
    
    **Customization Options:**
    - Professional, casual, enthusiastic, or formal tone
    - Short (150 words), medium (250 words), or long (400 words)
    - Specific skills or experiences to highlight
    """,
    response_model=CoverLetterResponse,
    tags=["AI Cover Letter Services"]
)
async def generate_cover_letter(
    cover_letter_request: CoverLetterRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate personalized cover letter."""
    return CoverLetterResponse(
        cover_letter=f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {cover_letter_request.position_title} position at {cover_letter_request.company_name}. With my background in software development and passion for innovative technology solutions, I am excited about the opportunity to contribute to your team.

[Generated cover letter content based on job description and user background...]

Thank you for considering my application. I look forward to discussing how my skills and enthusiasm can benefit {cover_letter_request.company_name}.

Sincerely,
[User Name]
        """.strip(),
        key_points_highlighted=[
            "Relevant technical skills",
            "Industry experience",
            "Company-specific interest",
            "Achievement metrics"
        ],
        suggestions=[
            "Consider adding a specific company achievement you admire",
            "Mention a relevant project from your portfolio",
            "Include a brief mention of your career goals"
        ]
    )


# === AI-POWERED INTERVIEW PREPARATION ===

@app.post(
    "/interview/prepare",
    summary="Generate interview preparation",
    description="""
    AI-powered interview preparation with tailored questions and insights.
    
    **Preparation Features:**
    - Role-specific interview questions
    - Company research insights
    - STAR method answer frameworks
    - Technical and behavioral questions
    - Difficulty-graded practice
    
    **Interview Types:**
    - General interviews
    - Technical assessments
    - Behavioral interviews
    - Case study discussions
    """,
    response_model=InterviewPrepResponse,
    tags=["AI Interview Services"]
)
async def prepare_interview(
    prep_request: InterviewPrepRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate interview preparation materials."""
    return InterviewPrepResponse(
        questions=[
            {
                "question": "Tell me about yourself and your experience with Python development.",
                "category": "general",
                "difficulty": "easy",
                "suggested_answer": "Focus on your relevant experience, key achievements, and why you're interested in this role.",
                "tips": [
                    "Keep it concise (2-3 minutes)",
                    "Structure: Present → Past → Future",
                    "Highlight relevant achievements"
                ]
            },
            {
                "question": "How would you optimize a slow-performing API endpoint?",
                "category": "technical",
                "difficulty": "medium",
                "suggested_answer": "Discuss profiling, database optimization, caching strategies, and code improvements.",
                "tips": [
                    "Show systematic problem-solving approach",
                    "Mention specific tools and techniques",
                    "Consider trade-offs in your solution"
                ]
            }
        ],
        company_insights=[
            f"{prep_request.company_name} values innovation and technical excellence",
            "Known for collaborative work environment",
            "Strong focus on work-life balance and professional development"
        ],
        preparation_tips=[
            "Research recent company news and achievements",
            "Prepare specific examples using STAR method",
            "Practice coding problems relevant to the role",
            "Prepare thoughtful questions about the role and company"
        ],
        research_suggestions=[
            f"Review {prep_request.company_name}'s recent product launches",
            "Check company leadership and team structure",
            "Look up interviewer backgrounds on LinkedIn",
            "Read employee reviews on Glassdoor"
        ]
    )


# === CAREER INSIGHTS AND ANALYTICS ===

@app.get(
    "/analytics/job-market",
    summary="Get job market analysis",
    description="""
    AI-powered job market analysis for specific skills and roles.
    
    **Market Insights:**
    - Skill demand scoring and trends
    - Average salary ranges by location
    - Growth projections and opportunities
    - Top hiring companies
    - Related skill recommendations
    """,
    response_model=List[JobMarketAnalysis],
    tags=["Career Analytics"]
)
async def get_job_market_analysis(
    skills: List[str],
    location: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get job market analysis for skills."""
    return [
        JobMarketAnalysis(
            skill="Python",
            demand_score=92.5,
            average_salary=125000,
            growth_trend="increasing",
            top_companies=["Google", "Microsoft", "Amazon", "Netflix"],
            related_skills=["FastAPI", "Django", "PostgreSQL", "Docker"]
        )
    ]


@app.post(
    "/analytics/career-advice",
    summary="Get career advancement advice",
    description="""
    AI-powered career advancement recommendations.
    
    **Advice Features:**
    - Skill gap analysis for target roles
    - Learning path recommendations
    - Timeline and milestone planning
    - Salary progression expectations
    - Networking and development tips
    """,
    response_model=CareerAdviceResponse,
    tags=["Career Analytics"]
)
async def get_career_advice(
    advice_request: CareerAdviceRequest,
    current_user: User = Depends(get_current_user)
):
    """Get personalized career advancement advice."""
    return CareerAdviceResponse(
        skill_gaps=["System Design", "Leadership", "Cloud Architecture"],
        learning_path=[
            "Complete system design course",
            "Lead a technical project",
            "Get AWS/Azure certification",
            "Practice technical mentoring"
        ],
        timeline_months=18,
        salary_expectations={
            "current_range": "100k-130k",
            "target_range": "140k-180k",
            "market_average": "160k"
        },
        recommended_certifications=[
            "AWS Solutions Architect",
            "Google Cloud Professional",
            "Certified Scrum Master"
        ],
        networking_tips=[
            "Join local tech meetups",
            "Contribute to open source projects",
            "Attend industry conferences",
            "Build relationships with current team leads"
        ]
    )


# === FILE UPLOAD SERVICES ===

@app.post(
    "/upload/resume",
    summary="Upload resume file",
    description="""
    Upload resume file for analysis and processing.
    
    **Supported Formats:**
    - PDF (.pdf)
    - Microsoft Word (.docx)
    - Plain text (.txt)
    
    **File Requirements:**
    - Maximum size: 10MB
    - Text must be readable (no images-only PDFs)
    """,
    response_model=FileUploadResponse,
    tags=["File Services"]
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload resume file."""
    return FileUploadResponse(
        file_id="resume_123456",
        filename=file.filename,
        file_size=len(await file.read()),
        file_type=file.content_type,
        upload_url=f"/files/resume_123456"
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with detailed error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.detail,
            details={"status_code": exc.status_code}
        ).dict()
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )