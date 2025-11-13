# Blog Posts API

A production-ready RESTful API for managing blog posts, built with Flask and SQLAlchemy. This API provides comprehensive CRUD operations with advanced features like pagination, search, filtering, and complete API documentation.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Configuration](#configuration)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [API Documentation](#api-documentation)
- [Testing](#testing)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Core Functionality
- **Complete CRUD Operations** - Create, read, update, and delete blog posts
- **Pagination** - Efficient handling of large datasets with customizable page sizes
- **Search & Filtering** - Search posts by title and content
- **Sorting** - Sort posts by creation date, update date, or title
- **Input Validation** - Comprehensive validation for all user inputs
- **Error Handling** - Robust error handling with meaningful error messages

### Technical Features
- **RESTful API Design** - Following REST best practices
- **Modular Architecture** - Clean separation of concerns with blueprints
- **Database Migrations** - Flask-Migrate for database version control
- **CORS Support** - Cross-Origin Resource Sharing enabled
- **API Documentation** - Interactive Swagger/OpenAPI documentation
- **Health Checks** - Health and ping endpoints for monitoring
- **Docker Support** - Full containerization with Docker and Docker Compose
- **Comprehensive Testing** - Complete test suite with pytest
- **Logging** - Structured logging for debugging and monitoring
- **Environment-based Configuration** - Separate configs for dev, test, and production

---

## Project Structure

```
Blog-Posts-Backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py         # Configuration classes
│   ├── models/
│   │   ├── __init__.py
│   │   └── post.py           # Post model and validation
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── posts.py          # Post endpoints
│   │   └── health.py         # Health check endpoints
│   └── utils/
│       ├── __init__.py
│       ├── errors.py         # Error handling utilities
│       └── pagination.py     # Pagination helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_posts.py         # Post endpoint tests
│   └── test_health.py        # Health check tests
├── docs/                     # Additional documentation
├── .env.example              # Example environment variables
├── .gitignore               # Git ignore rules
├── .dockerignore            # Docker ignore rules
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
└── README.md               # This file
```

---

## Tech Stack

- **Language:** Python 3.11+
- **Web Framework:** Flask 3.0.0
- **ORM:** SQLAlchemy 2.0.23
- **Database:** SQLite (development), PostgreSQL/MySQL (production)
- **Migrations:** Flask-Migrate 4.0.5
- **API Docs:** Flasgger 0.9.7.1 (Swagger/OpenAPI)
- **CORS:** Flask-CORS 4.0.0
- **Testing:** pytest 7.4.3, pytest-flask 1.3.0
- **Code Quality:** Black, Flake8
- **Server:** Gunicorn 21.2.0 (production)
- **Containerization:** Docker, Docker Compose

---

## Installation

### Local Setup

#### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

#### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/UNC-GDSC/Blog-Posts-Backend.git
   cd Blog-Posts-Backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   flask db init     # First time only
   flask db migrate  # Create migrations
   flask db upgrade  # Apply migrations
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000`

### Docker Setup

#### Prerequisites
- Docker
- Docker Compose

#### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/UNC-GDSC/Blog-Posts-Backend.git
   cd Blog-Posts-Backend
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

   The API will be available at `http://localhost:5000`

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the application**
   ```bash
   docker-compose down
   ```

---

## Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env` and customize:

```bash
# Flask Configuration
FLASK_ENV=development          # development, testing, or production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key     # Change in production!

# Database
DATABASE_URI=sqlite:///blog.db
# PostgreSQL: postgresql://user:pass@localhost:5432/blog_db
# MySQL: mysql://user:pass@localhost:3306/blog_db

# Pagination
POSTS_PER_PAGE=10
```

---

## Usage

### API Endpoints

All endpoints are prefixed with `/api/v1`

#### Health Checks

| Method | Endpoint  | Description                    |
|--------|-----------|--------------------------------|
| GET    | /health   | Comprehensive health check     |
| GET    | /ping     | Simple ping endpoint           |

#### Blog Posts

| Method | Endpoint              | Description                      |
|--------|-----------------------|----------------------------------|
| GET    | /api/v1/posts         | Get all posts (with pagination)  |
| GET    | /api/v1/posts/:id     | Get a specific post              |
| POST   | /api/v1/posts         | Create a new post                |
| PUT    | /api/v1/posts/:id     | Update a post                    |
| DELETE | /api/v1/posts/:id     | Delete a post                    |

#### Query Parameters (GET /api/v1/posts)

- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10, max: 100)
- `search` - Search term for title and content
- `sort` - Sort field: `created_at`, `updated_at`, `title` (default: `created_at`)
- `order` - Sort order: `asc`, `desc` (default: `desc`)

#### Examples

**Get all posts (paginated)**
```bash
curl http://localhost:5000/api/v1/posts
```

**Search posts**
```bash
curl http://localhost:5000/api/v1/posts?search=flask&page=1&per_page=10
```

**Create a post**
```bash
curl -X POST http://localhost:5000/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Post content here"}'
```

**Update a post**
```bash
curl -X PUT http://localhost:5000/api/v1/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

**Delete a post**
```bash
curl -X DELETE http://localhost:5000/api/v1/posts/1
```

#### Response Format

**Success Response (GET /api/v1/posts)**
```json
{
  "items": [
    {
      "id": 1,
      "title": "My First Post",
      "content": "This is the content.",
      "created_at": "2025-11-13T12:00:00",
      "updated_at": "2025-11-13T12:00:00"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total_items": 100,
    "total_pages": 10,
    "has_next": true,
    "has_prev": false,
    "next_page": "http://localhost:5000/api/v1/posts?page=2&per_page=10"
  }
}
```

**Error Response**
```json
{
  "error": "Validation Error",
  "message": "Title is required"
}
```

### API Documentation

Interactive API documentation is available via Swagger UI:

```
http://localhost:5000/api/docs
```

---

## Testing

The project includes a comprehensive test suite using pytest.

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Tests
```bash
# Test a specific file
pytest tests/test_posts.py

# Test a specific class
pytest tests/test_posts.py::TestCreatePost

# Test a specific function
pytest tests/test_posts.py::TestCreatePost::test_create_post_success
```

### View Coverage Report
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Development

### Code Formatting

Format code with Black:
```bash
black app/ tests/
```

### Linting

Check code style with Flake8:
```bash
flake8 app/ tests/
```

### Database Migrations

Create a new migration:
```bash
flask db migrate -m "Description of changes"
```

Apply migrations:
```bash
flask db upgrade
```

Rollback migrations:
```bash
flask db downgrade
```

---

## Deployment

### Production Considerations

1. **Environment Variables**
   - Set `FLASK_ENV=production`
   - Use a strong `SECRET_KEY`
   - Configure production database (PostgreSQL/MySQL)

2. **Database**
   - Use PostgreSQL or MySQL instead of SQLite
   - Set up regular backups
   - Configure connection pooling

3. **Server**
   - Use Gunicorn or uWSGI
   - Set up reverse proxy (Nginx/Apache)
   - Enable HTTPS with SSL certificates

4. **Monitoring**
   - Set up logging to files or external service
   - Use health check endpoints for monitoring
   - Configure alerting

### Deploy with Docker

```bash
# Build production image
docker build -t blog-api:latest .

# Run with production settings
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URI=postgresql://... \
  --name blog-api \
  blog-api:latest
```

### Deploy to Cloud Platforms

- **Heroku**: Use the included `Procfile` and buildpacks
- **AWS Elastic Beanstalk**: Deploy with Docker or Python platform
- **Google Cloud Run**: Build and deploy container
- **Azure App Service**: Deploy with Docker or Python runtime

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure tests pass: `pytest`
5. Format code: `black app/ tests/`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/UNC-GDSC/Blog-Posts-Backend/issues)
- **Discussions**: [GitHub Discussions](https://github.com/UNC-GDSC/Blog-Posts-Backend/discussions)

---

## Acknowledgments

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Flasgger](https://github.com/flasgger/flasgger) - API documentation

---

**Happy Coding!** 🚀
