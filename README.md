# PetikSendiri Backend

Backend API untuk aplikasi PetikSendiri menggunakan FastAPI.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **JWT** - Authentication

## Project Structure

```
petik-sendiri-be/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   └── env.py                  # Alembic environment config
├── app/
│   ├── api/                    # API endpoints
│   │   ├── v1/
│   │   │   ├── endpoints/      # Route handlers
│   │   │   │   ├── auth.py     # Authentication endpoints
│   │   │   │   └── users.py    # User endpoints
│   │   │   └── router.py       # API router
│   │   └── deps.py             # Dependencies (auth, etc.)
│   ├── core/                   # Core configurations
│   │   ├── config.py           # App settings
│   │   └── security.py         # Security utilities
│   ├── db/                     # Database
│   │   └── base.py             # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   └── user.py             # User model
│   ├── schemas/                # Pydantic schemas
│   │   └── user.py             # User schemas
│   ├── services/               # Business logic
│   │   └── user_service.py     # User service
│   └── main.py                 # FastAPI application
├── seeds/                      # Database seeders
│   ├── user_seeder.py          # User seeder
│   └── run_all_seeders.py      # Run all seeders
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
alembic upgrade head
```

### 4. Seed Database

```bash
python seeds/run_all_seeders.py
```

### 5. Run Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Demo User Credentials

After running the seeder, you can login with:

- **Email**: demo@petiksendiri.com
- **Password**: demo123

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/` - Get all users (authenticated)
- `GET /api/v1/users/me` - Get current user (authenticated)
- `GET /api/v1/users/{user_id}` - Get user by ID (authenticated)
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user (authenticated)
- `DELETE /api/v1/users/{user_id}` - Delete user (superuser only)

## Environment Variables

| Variable | Description |
|----------|-------------|
| DATABASE_HOST | Database host |
| DATABASE_PORT | Database port |
| DATABASE_USER | Database username |
| DATABASE_PASSWORD | Database password |
| DATABASE_NAME | Database name |
| SECRET_KEY | JWT secret key |
| ALGORITHM | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time |
