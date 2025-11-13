# Changelog

All notable changes to the Blog Posts API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-13

### Added - Major Feature Release

#### Database & Models
- **Tags System**: Added Tag model with many-to-many relationship to posts
- **Categories System**: Added Category model with hierarchical structure support
- **Soft Deletes**: Implemented soft delete functionality for posts
- **Database Indexes**: Added indexes on frequently queried fields (title, created_at, category_id)
- **Post Publishing**: Added is_published flag for draft/published state management

#### API Features
- **Rate Limiting**: Implemented Flask-Limiter for API rate limiting (200/day, 50/hour default)
- **Enhanced Error Handling**: Custom error classes with detailed error messages
- **Performance Monitoring**: Added middleware to track request timing and log slow requests
- **Security Headers**: Automatic security headers on all responses (X-Content-Type-Options, X-Frame-Options, etc.)
- **Request ID Tracking**: X-Request-ID header for request tracing

#### CLI Commands
- `flask seed-db`: Seed database with sample posts using Faker
- `flask clear-db`: Clear all posts from database
- `flask db-stats`: Display database statistics
- `flask export-posts`: Export posts to JSON or CSV format
- `flask backup-db`: Create database backup (SQLite)
- `flask create-admin`: Placeholder for future admin user creation

#### Development Tools
- **Makefile**: Comprehensive Makefile with common development tasks
- **Pre-commit Hooks**: Configured pre-commit hooks for code quality (Black, Flake8, Bandit, isort)
- **GitHub Actions**: Complete CI/CD pipeline with testing, linting, security scans, and Docker builds
- **Docker Compose Production**: Separate production configuration with PostgreSQL, Redis, and Nginx

#### Documentation
- **Postman Collection**: Complete API collection for testing
- **API Client Examples**:
  - Python client with full API coverage
  - JavaScript/Node.js client
  - Shell script with cURL examples
- **CHANGELOG**: This file for tracking changes
- **Examples README**: Comprehensive guide for using client examples

#### Infrastructure
- **Nginx Configuration**: Production-ready reverse proxy configuration
- **Multi-environment Docker**: Separate Docker Compose files for dev and production
- **Redis Support**: Optional Redis integration for caching and rate limiting (production)
- **PostgreSQL Support**: Production-ready PostgreSQL configuration

#### Code Quality
- **Type Validation**: Enhanced validation using marshmallow schemas
- **Security Scanning**: Bandit and Safety integration for security checks
- **Code Formatting**: Black and isort for consistent code style
- **Linting**: Flake8 configuration with project-specific rules

### Changed

#### Architecture
- Restructured application with modular blueprint-based design
- Implemented application factory pattern
- Separated concerns into distinct modules (models, routes, utils, config)

#### API
- Updated Post model with new fields (category_id, is_published, is_deleted)
- Enhanced Post.to_dict() to include category and tags
- Improved pagination with better metadata

#### Configuration
- Environment-based configuration (development, testing, production)
- Support for multiple database backends (SQLite, PostgreSQL, MySQL)
- Configurable rate limiting storage (memory, Redis)

#### Docker
- Updated Docker configuration with non-root user for security
- Enhanced health checks
- Improved multi-stage builds
- Added nginx service to docker-compose

### Security

- Added comprehensive security headers
- Implemented rate limiting to prevent abuse
- Security scanning in CI/CD pipeline
- Non-root Docker containers
- Input validation and sanitization

### Performance

- Added database indexes for improved query performance
- Request/response timing middleware
- Slow query logging
- Gzip compression in Nginx
- Connection pooling support

### Developer Experience

- One-command setup with Makefile
- Automated testing in CI/CD
- Pre-commit hooks for code quality
- Comprehensive documentation
- Client libraries in multiple languages
- Interactive API documentation with Swagger

## [1.0.0] - 2025-11-13

### Added

#### Core Features
- RESTful API for blog posts management
- Complete CRUD operations (Create, Read, Update, Delete)
- Pagination support with customizable page sizes
- Search functionality for posts
- Sorting by multiple fields (created_at, updated_at, title)
- Health check endpoints (/health, /ping)

#### Models
- Post model with title, content, timestamps
- SQLAlchemy ORM integration
- Automatic timestamp management

#### API Documentation
- Swagger/OpenAPI documentation with Flasgger
- Interactive API explorer at /api/docs

#### Testing
- Comprehensive test suite with pytest
- Test fixtures and configurations
- Coverage reporting
- Tests for all endpoints

#### Infrastructure
- Docker support with Dockerfile
- Docker Compose configuration
- Flask-Migrate for database migrations
- CORS support for cross-origin requests

#### Documentation
- Comprehensive README
- API endpoint documentation
- Installation and setup guides
- Deployment instructions
- Contributing guidelines
- MIT License

#### Configuration
- Environment variable support
- Separate configs for dev, test, production
- .env file support with python-dotenv

### Technical Stack

- Flask 3.0.0
- SQLAlchemy 2.0.23
- PostgreSQL/MySQL support (SQLite for dev)
- Gunicorn for production
- Python 3.11+

---

## Upgrade Guide

### From 1.0.0 to 2.0.0

#### Database Migrations

The 2.0.0 release introduces new models and fields. Run migrations:

```bash
flask db upgrade
```

#### New Environment Variables

Add to your `.env` file:

```bash
# Rate limiting (optional, defaults to memory)
RATELIMIT_STORAGE_URL=redis://localhost:6379

# Pagination (optional, default: 10)
POSTS_PER_PAGE=10
```

#### Breaking Changes

1. **Post Model**: New fields added (category_id, is_published, is_deleted)
   - Existing posts will have default values
   - `to_dict()` now includes category and tags

2. **API Responses**: Posts now include category and tags in responses

3. **Dependencies**: New required packages (see requirements.txt)
   - Flask-Limiter for rate limiting
   - Faker for CLI seed command
   - Additional dev dependencies

#### Migration Steps

1. Backup your database
2. Update dependencies: `pip install -r requirements.txt`
3. Run migrations: `flask db upgrade`
4. Update environment variables
5. Test the application
6. Deploy

---

For more information, see the [README](README.md) and [documentation](docs/).
