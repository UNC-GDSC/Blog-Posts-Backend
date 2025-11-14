"""Error handling utilities."""
from flask import jsonify
from werkzeug.exceptions import HTTPException


class ValidationError(Exception):
    """Custom validation error exception."""

    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code


class NotFoundError(Exception):
    """Custom not found error exception."""

    def __init__(self, message="Resource not found", status_code=404):
        super().__init__()
        self.message = message
        self.status_code = status_code


def handle_error(error):
    """
    Global error handler.

    Args:
        error: Exception instance

    Returns:
        JSON response with error details
    """
    if isinstance(error, ValidationError):
        response = {
            'error': 'Validation Error',
            'message': error.message
        }
        return jsonify(response), error.status_code

    if isinstance(error, NotFoundError):
        response = {
            'error': 'Not Found',
            'message': error.message
        }
        return jsonify(response), error.status_code

    if isinstance(error, HTTPException):
        response = {
            'error': error.name,
            'message': error.description
        }
        return jsonify(response), error.code

    # Handle unexpected errors
    response = {
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }
    return jsonify(response), 500


def register_error_handlers(app):
    """
    Register error handlers with Flask app.

    Args:
        app: Flask application instance
    """
    app.register_error_handler(ValidationError, handle_error)
    app.register_error_handler(NotFoundError, handle_error)
    app.register_error_handler(HTTPException, handle_error)
    app.register_error_handler(Exception, handle_error)
