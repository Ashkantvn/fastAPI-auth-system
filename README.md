# fastAPI-auth-system

**Description:** A compact authentication system built with FastAPI that provides user signup, login, profile, logout and account deletion endpoints. Designed for learning and as a starting point for production-ready auth services.

**Skills:**
- FastAPI (REST API design)
- SQLAlchemy (ORM + models)
- JWT (token creation and verification)
- Password hashing (bcrypt / passlib)
- Docker & Docker Compose
- pytest (API tests)

**Folder Structure:**
- `core/`: application package containing main app and submodules
	- `core/main.py`: FastAPI app and router registrations
	- `core/routers/`: API route handlers (e.g., `users.py`)
	- `core/utils/`: utilities (JWT manager, password manager, exceptions)
	- `core/models/`: database models for users and base schemas
	- `core/tests/`: pytest test suite for routes, database, and db models
- `Dockerfile.dev` / `docker-compose.yml`: containerization and development compose
- `requirements.txt`: Python dependencies
- `README.md`: this file
