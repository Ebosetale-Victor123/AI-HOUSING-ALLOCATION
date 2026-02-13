# AI-Driven University Hostel Allocation Engine

A Django-based backend system that uses Machine Learning to automate and optimize university hostel allocation based on student priority factors including academic merit, geographical distance, disability status, and financial need.

## Key AI Capabilities

- **Predictive Priority Scoring**: Calculates allocation priority (0-100) based on academic merit, geographical distance, disability status, and financial need
- **Constraint Satisfaction**: Ensures gender compliance, disability accessibility, and room capacity limits
- **Automated Allocation Engine**: Batch processing of thousands of applications with manual override functionality
- **Bias Detection**: Audit trails showing allocation rationale for transparency

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Backend Requirements](#2-backend-requirements)
3. [System Architecture](#3-system-architecture)
4. [Database Schema](#4-database-schema)
5. [Folder Structure](#5-folder-structure)
6. [Machine Learning Implementation](#6-machine-learning-implementation)
7. [API Endpoints Structure](#7-api-endpoints-structure)
8. [Key Implementation Details](#8-key-implementation-details)
9. [Environment Setup](#9-environment-setup)
10. [Frontend Integration Notes](#10-frontend-integration-notes)
11. [Testing Strategy](#11-testing-strategy)

---

## 1. System Overview

### Core Technologies

| Component | Technology |
|-----------|------------|
| Framework | Django 5.0+ (Python 3.11+) |
| API Layer | Django REST Framework (DRF) 3.14+ |
| Database | PostgreSQL 15+ (Production) / SQLite (Development) |
| ML/AI Stack | Scikit-learn 1.3+, Pandas 2.0+, Joblib 1.3+, NumPy 1.24+ |
| Task Queue | Celery 5.3+ + Redis 7+ (For batch allocation processing) |
| Authentication | JWT (SimpleJWT) + Django Guardian (Object-level permissions) |
| Documentation | Drf-spectacular (OpenAPI 3.0) |

### Infrastructure Requirements

- **Memory**: 4GB RAM minimum (8GB recommended for model training)
- **Storage**: Minimum 10GB (ML models, student documents)
- **Python Environment**: Virtualenv or Conda
- **Email service** (SMTP/SendGrid) for allocation notifications
- **Optional**: Google Maps API (for distance calculation verification)

### Security & Compliance

- **Role-Based Access Control (RBAC)**:
  - Super Admin (System configuration)
  - Housing Officer (Run allocations, manual overrides)
  - Student (View own application only)
- **Data Protection**: GDPR-compliant data handling (encryption at rest)
- **Audit Logging**: All allocation decisions logged with explainability metrics

---

## 2. Backend Requirements

```
Python 3.11+
Django 5.0+
Django REST Framework 3.14+
PostgreSQL 15+ (Production)
Redis 7+
Celery 5.3+
```

See `requirements/` directory for full dependency lists.

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (React Frontend - Managed by separate dev team)            │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS/REST
┌──────────────────────▼──────────────────────────────────────┐
│                    API Gateway Layer                         │
│  • Django REST Framework                                     │
│  • JWT Authentication                                        │
│  • Rate Limiting (Throttle classes)                          │
│  • Input Validation (Serializers)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
│   Business   │ │    ML    │ │   Task      │
│    Logic     │ │  Engine  │ │   Queue     │
│   Layer      │ │  Layer   │ │  (Celery)   │
└───────┬──────┘ └────┬─────┘ └──────┬──────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Data Persistence Layer                     │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────────┐ │
│  │  PostgreSQL  │ │  File Store  │ │   Redis Cache       │ │
│  │  (Primary)   │ │ (ML Models)  │ │   (Sessions/Queue)  │ │
│  └──────────────┘ └──────────────┘ └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 AI/ML Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ML Pipeline Flow                           │
└─────────────────────────────────────────────────────────────┘

[Data Ingestion] → [Feature Engineering] → [Model Training]
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│ Synthetic   │    │ GPA_Normalize│    │ Random Forest   │
│ Data Gen    │    │ Distance_Enc │    │ Regressor       │
│ (Bootstrap) │    │ Binary_Encode│    │ (Priority Score)│
└─────────────┘    └──────────────┘    └─────────────────┘
                                              │
[Prediction API] ← [Model Registry] ← [Serialization]
       │                  │
       ▼                  ▼
┌─────────────┐    ┌──────────────┐
│ Real-time   │    │ Versioning   │
│ Scoring     │    │ (joblib)     │
│ Endpoint    │    └──────────────┘
└─────────────┘
```

### 3.3 Allocation Algorithm Flow

```
    TRIGGER: Admin initiates allocation cycle
         │
         ▼
    FILTERING: Remove ineligible applications
         • Gender mismatches
         • Incomplete profiles
         • Previous allocation status
         │
         ▼
    FEATURE EXTRACTION: Transform data for ML
         • Normalize GPA (0.0-5.0 → 0-1)
         • Encode categorical (Level, Disability)
         • Calculate distance metrics
         │
         ▼
    ML INFERENCE: Generate Priority Scores (0-100)
         • Load pre-trained model (model.pkl)
         • Batch prediction via Celery
         • Store scores with confidence intervals
         │
         ▼
    CONSTRAINT SOLVING: Room Assignment
         • Sort by Priority Score (Desc)
         • Match disabled students → Accessible rooms
         • Match gender → Gender-specific hostels
         • Fill rooms by capacity
         │
         ▼
    PERSISTENCE: Atomic transaction commit
         • Update Room occupancy
         • Update Application status
         • Generate allocation records
         │
         ▼
    NOTIFICATION: Async email dispatch
```

---

## 4. Database Schema (Entity Relationship)

### Core Entities

#### User (AbstractUser)
| Field | Type | Description |
|-------|------|-------------|
| `email` | String | Unique identifier |
| `matric_number` | String | Unique, for students |
| `user_type` | Enum | Student, Admin, SuperAdmin |
| `department` | String | Academic department |
| `phone_number` | String | Contact number |
| `is_verified` | Boolean | Email verification status |

#### StudentProfile
| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOne | Link to User model |
| `current_gpa` | Decimal | 3,2 decimal places |
| `level` | Integer | 100, 200, 300, 400, 500 |
| `home_address` | Text | Home address |
| `distance_from_campus` | Float | Auto-calculated km |
| `disability_status` | Boolean | Accessibility needs |
| `disability_details` | Text | Optional details |
| `financial_aid_status` | Boolean | Financial need indicator |
| `gender` | Enum | M/F |
| `date_of_birth` | Date | Birth date |

#### Hostel
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Hostel name |
| `gender_type` | Enum | Male/Female/Mixed |
| `total_rooms` | Integer | Total room count |
| `warden_name` | Char | Warden in charge |
| `location_lat/lng` | Float | GPS coordinates (optional) |

#### Room
| Field | Type | Description |
|-------|------|-------------|
| `hostel` | ForeignKey | Parent hostel |
| `room_number` | Char | Room identifier |
| `capacity` | Integer | Default 4 |
| `current_occupancy` | Integer | Default 0 |
| `floor_level` | Integer | Floor number |
| `is_accessible` | Boolean | Disability access |
| `room_type` | Enum | Standard, Premium, Medical |

#### Application (Core Transaction Entity)
| Field | Type | Description |
|-------|------|-------------|
| `student` | ForeignKey | Applicant |
| `academic_session` | Char | e.g., "2024/2025" |
| `preferred_hostel` | ForeignKey | Optional preference |
| `status` | Enum | Pending/Approved/Rejected/Allocated |
| `priority_score` | Float | AI-generated (0-100) |
| `ai_confidence` | Float | Model confidence (0-1) |
| `allocation_date` | DateTime | When allocated |
| `created_at` | DateTime | Application timestamp |
| `medical_certificate` | FileField | Optional documentation |

#### Allocation (Final Assignment)
| Field | Type | Description |
|-------|------|-------------|
| `application` | OneToOne | Linked application |
| `room` | ForeignKey | Assigned room |
| `bed_space_number` | Integer | Specific bed space |
| `allocated_by` | Char | "AI_System" or "Admin_User" |
| `allocation_reason` | Text | Explainability note |
| `admin_override` | Boolean | Manual override flag |

#### AuditLog
| Field | Type | Description |
|-------|------|-------------|
| `action` | Char | Action performed |
| `user` | ForeignKey | Actor |
| `timestamp` | DateTime | When occurred |
| `ip_address` | IPAddress | Source IP |
| `details` | JSONField | Additional context |

---

## 5. Folder Structure

```
smartalloc-backend/
├── apps/
│   ├── __init__.py
│   ├── users/                          # Custom User model + Auth
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── students/                       # Student profiles
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── hostels/                        # Hostel & Room management
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── admin_views.py              # Admin-only endpoints
│   │   └── urls.py
│   ├── applications/                   # Application lifecycle
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   └── allocation/                     # Core AI/ML Engine
│       ├── models.py                   # Allocation & Audit models
│       ├── ml_models/                  # ML scripts & artifacts
│       │   ├── __init__.py
│       │   ├── training_pipeline.py    # Synthetic data + training
│       │   ├── predictor.py            # Real-time inference
│       │   ├── features.py             # Feature engineering
│       │   └── artifacts/              # Saved models
│       │       ├── housing_model_v1.pkl
│       │       └── scaler.pkl
│       ├── allocation_engine.py        # Core assignment algorithm
│       ├── tasks.py                    # Celery async tasks
│       ├── serializers.py
│       ├── views.py                    # API endpoints
│       └── urls.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py                         # Root URL conf
│   ├── wsgi.py
│   └── celery.py                       # Celery configuration
├── utils/
│   ├── __init__.py
│   ├── constants.py                    # Enums, choices
│   ├── permissions.py                  # Custom DRF permissions
│   ├── exceptions.py                   # Custom exceptions
│   └── validators.py                   # Custom validators
├── scripts/
│   ├── setup_db.sh                     # Initial DB setup
│   ├── train_model.sh                  # Trigger ML training
│   └── seed_data.py                    # Generate synthetic data
├── requirements/
│   ├── base.txt                        # Core requirements
│   ├── dev.txt                         # Dev + Testing
│   └── prod.txt                        # Production
├── notebooks/                          # Jupyter notebooks for ML
│   ├── EDA.ipynb                       # Exploratory Data Analysis
│   └── model_optimization.ipynb        # Hyperparameter tuning
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── media/                              # User uploads (docs)
├── static/                             # Admin static files
├── logs/                               # Application logs
├── manage.py
├── README.md
└── .env.example                        # Environment variables template
```

---

## 6. Machine Learning Implementation

### 6.1 Feature Engineering Strategy

**Input Features (X):**

| Feature | Type | Description |
|---------|------|-------------|
| `gpa_normalized` | Float | 0.0-1.0 scale |
| `level_encoded` | Integer | 100=1, 200=2, 300=3, 400=4, 500=5 |
| `distance_km` | Float | Continuous, log-transformed |
| `disability_flag` | Binary | 0/1 |
| `financial_aid_flag` | Binary | 0/1 |
| `seniority_score` | Derived | Level * GPA |

**Target Variable (y):**
- `priority_score` (0-100, synthetic generation for training)

### 6.2 Model Selection

| Aspect | Choice |
|--------|--------|
| Algorithm | Random Forest Regressor (Ensemble, handles non-linear relationships) |
| Alternative | Gradient Boosting (XGBoost) if higher accuracy needed |
| Rationale | Interpretable feature importance, handles mixed data types, robust to outliers |

### 6.3 Training Data Strategy

Since historical data doesn't exist initially:

```python
# Synthetic Data Generation Logic
def generate_training_data(n=5000):
    data = {
        'gpa': np.random.uniform(0.0, 5.0, n),
        'level': np.random.choice([100, 200, 300, 400, 500], n),
        'distance': np.random.exponential(50, n),  # km
        'disability': np.random.choice([0, 1], n, p=[0.95, 0.05]),
        'financial_aid': np.random.choice([0, 1], n, p=[0.7, 0.3])
    }
    
    # Synthetic priority formula (domain knowledge)
    # 40% GPA, 30% Distance, 20% Level, 10% Need-based
    priority = (
        (data['gpa'] / 5.0) * 40 +
        (min(data['distance'], 500) / 500) * 30 +
        (data['level'] / 500) * 20 +
        ((data['disability'] + data['financial_aid']) > 0) * 10
    )
    return data, priority
```

### 6.4 Model Persistence

| Aspect | Details |
|--------|---------|
| Format | Joblib (Python-specific, efficient for sklearn) |
| Versioning | Semantic versioning (v1.0.0, v1.1.0) |
| Storage | File system (media/ml_models/) with database registry tracking |

### 6.5 Prediction Service API

```python
# apps/allocation/ml_models/predictor.py
class PriorityPredictor:
    def __init__(self, model_path='artifacts/housing_model_v1.pkl'):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load('artifacts/scaler.pkl')
    
    def predict(self, student_features: dict) -> dict:
        """
        Returns: {
            'priority_score': float,
            'confidence': float,
            'feature_importance': dict
        }
        """
        # Preprocessing logic
        # Model inference
        # Post-processing (clamping 0-100)
        pass
```

---

## 7. API Endpoints Structure

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Student registration |
| POST | `/api/auth/login/` | JWT token obtain |
| POST | `/api/auth/refresh/` | Token refresh |

### Student Portal

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/profile/` | Retrieve profile |
| PUT | `/api/students/profile/` | Update profile |
| POST | `/api/applications/submit/` | Submit housing application |
| GET | `/api/applications/status/` | Check application status |

### Admin/Housing Officer

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/hostels/` | CRUD Hostels |
| GET | `/api/admin/rooms/` | CRUD Rooms |
| POST | `/api/admin/allocation/run/` | Trigger AI Allocation |
| GET | `/api/admin/allocation/results/` | View allocations |
| POST | `/api/admin/allocation/override/` | Manual override |
| GET | `/api/admin/analytics/dashboard/` | Statistics & reports |

### ML System

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ml/train/` | Retrain model (Admin only) |
| GET | `/api/ml/model-status/` | Current model metrics |
| POST | `/api/ml/predict-single/` | Test prediction (Debug) |

---

## 8. Key Implementation Details

### 8.1 Allocation Algorithm Constraints

```python
CONSTRAINTS = {
    'gender_strict': True,        # No mixed-gender hostels
    'disability_priority': True,  # Auto top-score for disabled
    'seniority_boost': 1.2,       # Multiplier for 400/500 level
    'max_distance_cap': 500,      # Max km for scoring
    'room_capacity_strict': True  # No overbooking
}
```

### 8.2 Asynchronous Processing

**Celery Tasks:**
- `process_batch_allocation()` - Heavy ML inference
- `send_allocation_emails()` - Bulk notifications
- `generate_audit_report()` - PDF report generation

### 8.3 Audit Trail Requirements

Every allocation decision must log:
- Input features (GPA, Distance, etc.)
- Model version used
- Raw model output vs Final score (if adjusted)
- Timestamp and Admin ID (if override)

---

## 9. Environment Setup

### 9.1 Local Development

```bash
# Clone repository
git clone <repo-url>
cd smartalloc-backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies
pip install -r requirements/dev.txt

# Database setup
createdb smartalloc_db
python manage.py migrate
python manage.py createsuperuser

# ML Model initialization
python scripts/seed_data.py  # Generate synthetic data
python apps/allocation/ml_models/training_pipeline.py

# Run server
python manage.py runserver
```

### 9.2 Production Deployment (Docker)

```bash
docker-compose -f docker/docker-compose.yml up --build
```

### 9.3 Environment Variables (.env)

```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/smartalloc
REDIS_URL=redis://localhost:6379/0
EMAIL_BACKEND=smtp
ML_MODEL_PATH=apps/allocation/ml_models/artifacts/
```

---

## 10. Frontend Integration Notes

**For the Frontend Developer:**

| Setting | Value |
|---------|-------|
| Base URL | `http://localhost:8000/api/` |
| Auth | `Authorization: Bearer <access_token>` header |
| Content-Type | `application/json` |
| File Uploads | Use `multipart/form-data` for medical certificates |
| CORS | Pre-configured for localhost:3000 (React default) |

**Key Frontend Flows:**

1. **Student submits application**
   - `POST /api/applications/submit/`

2. **Admin triggers allocation**
   - `POST /api/admin/allocation/run/` (Returns task_id)
   - Poll for status → `GET /api/admin/allocation/status/<task_id>/`

3. **Fetch results**
   - `GET /api/admin/allocation/results/`

**Optional WebSocket:** `/ws/allocation-status/` for real-time allocation progress updates

---

## 11. Testing Strategy

| Test Type | Tool | Criteria |
|-----------|------|----------|
| Unit Tests | pytest | ML model accuracy (>85% threshold) |
| Integration Tests | Django test client | API endpoint coverage |
| Load Tests | Locust | 1000+ concurrent applications |
| ML Validation | K-fold cross-validation | On synthetic dataset |

---

## License

[Your License Here]

## Contributors

[Your Team/Contributors Here]

## Support

For technical support or questions, contact: [support-email@university.edu]
