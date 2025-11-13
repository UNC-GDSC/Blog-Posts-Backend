# Contributing to Blog Posts API

Thank you for your interest in contributing to the Blog Posts API! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/Blog-Posts-Backend.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Development Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations:**
   ```bash
   flask db upgrade
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

## Making Changes

1. **Keep changes focused:** Each pull request should address a single concern
2. **Write clear commit messages:** Use descriptive commit messages that explain what and why
3. **Update documentation:** Update README.md and docstrings as needed
4. **Add tests:** Include tests for new features or bug fixes

## Testing

Run the test suite before submitting your changes:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_posts.py

# Run specific test
pytest tests/test_posts.py::TestCreatePost::test_create_post_success
```

## Code Style

We follow PEP 8 style guidelines for Python code.

1. **Format your code:**
   ```bash
   black app/ tests/
   ```

2. **Check code style:**
   ```bash
   flake8 app/ tests/
   ```

3. **General guidelines:**
   - Use 4 spaces for indentation
   - Maximum line length of 88 characters (Black's default)
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Keep functions focused and small

## Submitting Changes

1. **Ensure tests pass:**
   ```bash
   pytest
   ```

2. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request:**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear description of your changes
   - Reference any related issues

### Pull Request Guidelines

- **Title:** Use a clear, descriptive title
- **Description:** Explain what changes you made and why
- **Tests:** Ensure all tests pass
- **Documentation:** Update relevant documentation
- **Single Responsibility:** Each PR should address one feature or bug

## Reporting Bugs

When reporting bugs, please include:

1. **Description:** Clear description of the bug
2. **Steps to Reproduce:** Detailed steps to reproduce the issue
3. **Expected Behavior:** What you expected to happen
4. **Actual Behavior:** What actually happened
5. **Environment:** Python version, OS, etc.
6. **Logs:** Relevant error messages or logs

## Suggesting Enhancements

When suggesting enhancements:

1. **Use Case:** Describe the use case for the enhancement
2. **Proposed Solution:** Explain your proposed solution
3. **Alternatives:** Mention any alternative solutions considered
4. **Benefits:** Explain the benefits of the enhancement

## Development Workflow

1. **Create an issue** for the feature or bug
2. **Discuss** the approach in the issue
3. **Fork** the repository
4. **Create a branch** from main
5. **Make changes** with tests
6. **Submit PR** referencing the issue
7. **Address review** comments
8. **Merge** once approved

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Reach out to the maintainers

Thank you for contributing to Blog Posts API!
