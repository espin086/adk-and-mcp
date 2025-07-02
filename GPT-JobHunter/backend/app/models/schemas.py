"""
Pydantic schemas for GPT-JobHunter API
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, validator


# Enums
class ApplicationStatus(str, Enum):
    """Job application status options."""
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobType(str, Enum):
    """Job type options."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class ExperienceLevel(str, Enum):
    """Experience level options."""
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


# Base Models
class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# User Models
class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update model."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class User(UserBase, TimestampMixin):
    """User response model."""
    id: int
    
    class Config:
        from_attributes = True


# Authentication Models
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[int] = None


# Profile Models
class ProfileBase(BaseModel):
    """Base profile model."""
    headline: Optional[str] = Field(None, max_length=200)
    summary: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    desired_salary_min: Optional[int] = Field(None, ge=0)
    desired_salary_max: Optional[int] = Field(None, ge=0)
    skills: List[str] = Field(default_factory=list)
    preferences: Dict[str, Any] = Field(default_factory=dict)


class ProfileCreate(ProfileBase):
    """Profile creation model."""
    pass


class ProfileUpdate(ProfileBase):
    """Profile update model."""
    pass


class Profile(ProfileBase, TimestampMixin):
    """Profile response model."""
    id: int
    user_id: int
    
    class Config:
        from_attributes = True


# Job Models
class JobBase(BaseModel):
    """Base job model."""
    title: str = Field(..., max_length=200)
    company: str = Field(..., max_length=100)
    description: str
    requirements: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    remote_allowed: bool = False
    skills_required: List[str] = Field(default_factory=list)
    url: Optional[str] = None
    source: Optional[str] = Field(None, max_length=50)


class JobCreate(JobBase):
    """Job creation model."""
    pass


class Job(JobBase, TimestampMixin):
    """Job response model."""
    id: int
    match_score: Optional[float] = Field(None, ge=0, le=100)
    
    class Config:
        from_attributes = True


# Job Search Models
class JobSearchRequest(BaseModel):
    """Job search request model."""
    query: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=100)
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    remote_only: bool = False
    skills: List[str] = Field(default_factory=list)
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)


class JobSearchResponse(BaseModel):
    """Job search response model."""
    jobs: List[Job]
    total: int
    page: int
    limit: int
    has_more: bool


# Application Models
class ApplicationBase(BaseModel):
    """Base application model."""
    job_id: int
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=1000)
    follow_up_date: Optional[datetime] = None


class ApplicationCreate(ApplicationBase):
    """Application creation model."""
    cover_letter: Optional[str] = None
    resume_version: Optional[str] = None


class ApplicationUpdate(BaseModel):
    """Application update model."""
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)
    follow_up_date: Optional[datetime] = None


class Application(ApplicationBase, TimestampMixin):
    """Application response model."""
    id: int
    user_id: int
    job: Job
    
    class Config:
        from_attributes = True


# Resume Models
class ResumeAnalysisRequest(BaseModel):
    """Resume analysis request model."""
    file_path: Optional[str] = None
    text_content: Optional[str] = None
    target_job_description: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response model."""
    strengths: List[str]
    weaknesses: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    ats_score: float = Field(..., ge=0, le=100)
    keyword_match: float = Field(..., ge=0, le=100)
    overall_score: float = Field(..., ge=0, le=100)


class ResumeOptimizationRequest(BaseModel):
    """Resume optimization request model."""
    current_resume: str
    target_job_description: str
    focus_areas: List[str] = Field(default_factory=list)


class ResumeOptimizationResponse(BaseModel):
    """Resume optimization response model."""
    optimized_resume: str
    changes_made: List[str]
    improvement_areas: List[str]


# Cover Letter Models
class CoverLetterRequest(BaseModel):
    """Cover letter generation request model."""
    job_description: str
    company_name: str
    position_title: str
    user_background: Optional[str] = None
    tone: str = Field("professional", pattern="^(professional|casual|enthusiastic|formal)$")
    length: str = Field("medium", pattern="^(short|medium|long)$")


class CoverLetterResponse(BaseModel):
    """Cover letter generation response model."""
    cover_letter: str
    key_points_highlighted: List[str]
    suggestions: List[str]


# Interview Models
class InterviewPrepRequest(BaseModel):
    """Interview preparation request model."""
    job_description: str
    company_name: str
    position_title: str
    interview_type: str = Field("general", pattern="^(general|technical|behavioral|case_study)$")
    experience_level: Optional[ExperienceLevel] = None


class InterviewQuestion(BaseModel):
    """Interview question model."""
    question: str
    category: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    suggested_answer: Optional[str] = None
    tips: List[str] = Field(default_factory=list)


class InterviewPrepResponse(BaseModel):
    """Interview preparation response model."""
    questions: List[InterviewQuestion]
    company_insights: List[str]
    preparation_tips: List[str]
    research_suggestions: List[str]


# Analytics Models
class JobMarketAnalysis(BaseModel):
    """Job market analysis model."""
    skill: str
    demand_score: float = Field(..., ge=0, le=100)
    average_salary: Optional[int] = None
    growth_trend: str = Field(..., pattern="^(increasing|stable|decreasing)$")
    top_companies: List[str] = Field(default_factory=list)
    related_skills: List[str] = Field(default_factory=list)


class CareerAdviceRequest(BaseModel):
    """Career advice request model."""
    current_role: str
    target_role: str
    experience_years: int = Field(..., ge=0, le=50)
    skills: List[str] = Field(default_factory=list)
    industry: Optional[str] = None


class CareerAdviceResponse(BaseModel):
    """Career advice response model."""
    skill_gaps: List[str]
    learning_path: List[str]
    timeline_months: int
    salary_expectations: Dict[str, int]
    recommended_certifications: List[str]
    networking_tips: List[str]


# File Upload Models
class FileUploadResponse(BaseModel):
    """File upload response model."""
    file_id: str
    filename: str
    file_size: int
    file_type: str
    upload_url: Optional[str] = None


# Error Models
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


# Success Models
class SuccessResponse(BaseModel):
    """Success response model."""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None