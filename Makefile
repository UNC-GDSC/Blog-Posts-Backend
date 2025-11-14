.PHONY: help install dev test coverage lint format clean run docker-build docker-up docker-down migrate seed

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

dev:  ## Install development dependencies
	pip install -r requirements.txt
	pre-commit install

test:  ## Run tests
	pytest

test-verbose:  ## Run tests with verbose output
	pytest -v

coverage:  ## Run tests with coverage report
	pytest --cov=app --cov-report=html --cov-report=term

lint:  ## Run linting checks
	flake8 app/ tests/
	black --check app/ tests/

format:  ## Format code with black
	black app/ tests/

security:  ## Run security checks
	safety check
	bandit -r app/

clean:  ## Clean up generated files
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build

run:  ## Run the development server
	python run.py

run-prod:  ## Run with gunicorn (production)
	gunicorn --bind 0.0.0.0:5000 --workers 4 run:app

docker-build:  ## Build Docker image
	docker build -t blog-api:latest .

docker-up:  ## Start Docker containers
	docker-compose up -d

docker-down:  ## Stop Docker containers
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f

migrate-init:  ## Initialize database migrations
	flask db init

migrate:  ## Create a new migration
	flask db migrate -m "$(msg)"

migrate-upgrade:  ## Apply migrations
	flask db upgrade

migrate-downgrade:  ## Rollback last migration
	flask db downgrade

seed:  ## Seed database with sample data
	flask seed-db --count=50

db-stats:  ## Show database statistics
	flask db-stats

backup:  ## Backup database
	flask backup-db

export-json:  ## Export posts to JSON
	flask export-posts --format=json --output=posts_export

export-csv:  ## Export posts to CSV
	flask export-posts --format=csv --output=posts_export

shell:  ## Start Flask shell
	flask shell

routes:  ## Show all routes
	flask routes

all: clean install test lint  ## Run all checks

ci: lint test coverage  ## Run CI pipeline locally
