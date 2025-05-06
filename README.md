# FastAPI Project Template

A template for building FastAPI applications with PostgreSQL, Redis OM, SQLAlchemy, JWT Authentication, and more.

## Features

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
*   **Database:** PostgreSQL (via `psycopg2-binary`)
*   **Authentication:** JWT Bearer Tokens (`PyJWT`, `passlib`)
*   **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
*   **Migrations:** Redis OM Migrator (included in `run.py`). *Note: Alembic is installed but setup might be needed for SQLAlchemy migrations.*
*   **Configuration:** Environment variables via `.env` file (`python-dotenv`)
*   **Logging:** [Loguru](https://github.com/Delgan/loguru)
*   **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)

## Prerequisites

*   Python 3.7+
*   uv (Future of Python package installer - using pip alone is slow)
*   A running PostgreSQL database instance.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Rename a `.env.example` file in the project root directory.
2.  Populate the `.env` file with the necessary environment variables:

    ```dotenv
    # API Settings
    API_DEBUG=True             # Set to False in production
    API_NAME="My FastAPI App"
    API_HOST=0.0.0.0           # Host to bind the server to
    API_PORT=8000              # Port to run the server on
    API_VERSION="0.1.0"
    AUTH_KEY="your_super_secret_jwt_key" # CHANGE THIS! Generate a strong secret key.
    HOST_URL="http://localhost:8000" # Base URL of the application

    # Database (Example for PostgreSQL)
    DATABASE_URL="postgresql+psycopg2://user:password@host:port/database_name"

    # Logging
    LOG_LEVEL="INFO"
    LOG_FORMAT="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>" # Example format
    MAX_BYTES=10485760 # Example: 10MB log rotation size
    ```

    *   **Important:** Replace placeholder values (like database credentials and `AUTH_KEY`) with your actual configuration.
    *   Ensure your `DATABASE_URL` points to your running PostgreSQL instance.

## Database Migrations

*   **SQLAlchemy (Alembic):** Alembic is installed (`alembic` in `requirements.txt`), but the standard setup ( `alembic.ini`, `env.py`, `versions` directory) might not be present. If you need to manage PostgreSQL schema migrations:
    1.  Initialize Alembic: `alembic init alembic` (if not already done).
    2.  Configure `alembic.ini` (set `sqlalchemy.url = %(DATABASE_URL)s`) and `env.py` (import your Base model and set `target_metadata`).
    3.  Create migrations: `alembic revision --autogenerate -m "Your migration message"`
    4.  Apply migrations: `alembic upgrade head`

## Running the Application

1.  Ensure your `.env` file is configured correctly.
2.  Make sure your PostgreSQL and Redis instances are running and accessible.
3.  Run the application using the `run.py` script:

    ```bash
    python run.py
    ```

    The server will start on the host and port specified in your `.env` file (e.g., `http://0.0.0.0:8000`).


## API Documentation

FastAPI provides automatic interactive API documentation. Once the server is running, access:

*   **Swagger UI:** `http://<your_host>:<your_port>/docs`
*   **ReDoc:** `http://<your_host>:<your_port>/redoc`

## Project Structure (Overview)

```
.
├── app/                # Core application module
│   ├── __init__.py     # FastAPI app initialization, middleware
│   ├── api/            # API endpoints (routers, schemas, views)
│   │   ├── admin/
│   │   ├── auth/
│   │   └── users/
│   ├── endpoint/       # Endpoint routing setup
│   │   ├── build_routes.py
│   │   └── urls.py
│   ├── models.py       # SQLAlchemy ORM models
│   └── shared/         # Shared utilities, middleware,  helpers
│       ├── authentication/
│       ├── bases/
│       ├── helpers/
│       └── middleware/
├── config/             # Configuration files
│   └── settings.py     # Application settings (reads .env)
├── .env                # Local environment variables (create this)
├── README.md           # This file
├── requirements.txt    # Project dependencies
└── run.py              # Application entry point (runs uvicorn)
``` 