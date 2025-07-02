# 🚀 GPT-JobHunter

An AI-powered job hunting assistant that helps you optimize your job search with cutting-edge technology. The application is built with a **decoupled architecture** featuring a FastAPI backend and Streamlit frontend.

## 🏗️ Architecture

This project follows a **microservices architecture** with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │   PostgreSQL    │
│   Frontend      │◄──►│    Backend      │◄──►│   Database      │
│   (Port 8501)   │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │              ┌─────────────────┐
         │                       └─────────────►│     Redis       │
         │                                      │     Cache       │
         │                                      │   (Port 6379)   │
         └──────────────────────────────────────┴─────────────────┘
```

### Components

- **Frontend (Streamlit)**: User-friendly web interface for job hunting features
- **Backend (FastAPI)**: RESTful API with comprehensive job hunting endpoints
- **Database (PostgreSQL)**: Data persistence for users, jobs, and applications
- **Cache (Redis)**: Fast caching and session management
- **Reverse Proxy (Nginx)**: Optional load balancing and SSL termination

## ✨ Features

### 🔍 **Smart Job Search**
- AI-powered job matching and recommendations
- Advanced filtering by location, salary, experience level
- Semantic search with intelligent keyword matching

### 📄 **Resume Services**
- AI-powered resume analysis and ATS compatibility scoring
- Resume optimization for specific job applications
- Keyword integration and formatting suggestions

### ✉️ **Cover Letter Generation**
- Personalized cover letters for each application
- Multiple tone and length options
- Company and role-specific content

### 🎯 **Interview Preparation**
- Tailored interview questions by role and company
- STAR method answer frameworks
- Company research and preparation tips

### 📊 **Career Analytics**
- Job market analysis and skill demand trends
- Career advancement recommendations
- Salary insights and growth projections

### 📋 **Application Tracking**
- Comprehensive job application management
- Status tracking and follow-up reminders
- Analytics and success metrics

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GPT-JobHunter
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the applications**
   - **Frontend**: http://localhost:8501
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

5. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variable**
   ```bash
   export API_BASE_URL=http://localhost:8000
   ```

5. **Start the frontend**
   ```bash
   streamlit run app.py
   ```

## 📚 API Documentation

The FastAPI backend provides comprehensive API documentation with interactive testing capabilities.

### Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

#### Profile Management
- `GET /profile` - Get user profile
- `POST /profile` - Create user profile
- `PUT /profile` - Update user profile

#### Job Search
- `POST /jobs/search` - Search for jobs with AI matching
- `GET /jobs/recommendations` - Get personalized job recommendations

#### AI Services
- `POST /resume/analyze` - AI-powered resume analysis
- `POST /resume/optimize` - Resume optimization for job applications
- `POST /cover-letter/generate` - Generate personalized cover letters
- `POST /interview/prepare` - Interview preparation with tailored questions

#### Analytics
- `GET /analytics/job-market` - Job market analysis for skills
- `POST /analytics/career-advice` - Career advancement recommendations

#### Application Tracking
- `GET /applications` - Get user's job applications
- `POST /applications` - Create new job application

### Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Rate Limits

- **Free Tier**: 100 requests/hour
- **Premium Tier**: 1000 requests/hour

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# API Configuration
DEBUG=true
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/jobhunter

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

### Docker Configuration

Customize the Docker setup by editing:
- `docker-compose.yml` - Service configuration
- `backend/Dockerfile` - Backend container setup
- `frontend/Dockerfile` - Frontend container setup

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
pytest tests/ -v
```

### API Testing

Use the interactive API documentation at http://localhost:8000/docs to test endpoints directly in your browser.

## 📁 Project Structure

```
GPT-JobHunter/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application
│   │   ├── config.py          # Configuration settings
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py     # Pydantic models
│   │   └── api/               # API endpoints
│   ├── requirements.txt       # Backend dependencies
│   └── Dockerfile            # Backend container
├── frontend/                  # Streamlit Frontend
│   ├── app.py                # Main Streamlit application
│   ├── requirements.txt      # Frontend dependencies
│   └── Dockerfile           # Frontend container
├── docker/                   # Docker configuration
│   └── nginx.conf           # Nginx configuration
├── docs/                    # Project documentation
├── tests/                   # Test files
├── docker-compose.yml       # Multi-service setup
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   DEBUG=false
   SECRET_KEY=your-secure-production-key
   DATABASE_URL=your-production-database-url
   ```

2. **Build and deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up SSL with Let's Encrypt**
   ```bash
   # Configure SSL in nginx.conf
   # Use certbot for SSL certificates
   ```

### Cloud Deployment Options

- **AWS ECS/Fargate**: Container orchestration
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Managed containers
- **DigitalOcean App Platform**: PaaS deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use type hints for better code quality
- Write comprehensive tests
- Update documentation for new features
- Ensure Docker builds work correctly

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **Architecture Guide**: [docs/architecture.md](docs/architecture.md)
- **Deployment Guide**: [docs/deployment.md](docs/deployment.md)

### Community
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Wiki**: Community-contributed guides

### Professional Support
- **Email**: support@gpt-jobhunter.com
- **Enterprise**: enterprise@gpt-jobhunter.com

---

## 🌟 Features in Detail

### AI-Powered Job Matching

Our sophisticated AI engine analyzes your profile, skills, and preferences to provide highly relevant job recommendations with match scores.

### Resume Optimization

Advanced NLP algorithms analyze your resume for:
- ATS (Applicant Tracking System) compatibility
- Keyword optimization
- Structure and formatting
- Content strength assessment

### Smart Cover Letter Generation

Generate compelling, personalized cover letters that:
- Match company culture and job requirements
- Highlight your relevant experience
- Use appropriate tone and style
- Include industry-specific keywords

### Interview Preparation

Comprehensive interview preparation featuring:
- Role-specific questions and answers
- Company research insights
- STAR method frameworks
- Practice scenarios and tips

### Career Analytics

Data-driven career insights including:
- Skill demand analysis
- Salary benchmarking
- Market trends and projections
- Career path recommendations

---

**Built with ❤️ by the GPT-JobHunter Team**