"""Application middleware."""
import time
from flask import request, g
import logging

logger = logging.getLogger(__name__)


def init_middleware(app):
    """
    Initialize middleware with Flask app.

    Args:
        app: Flask application instance
    """

    @app.before_request
    def before_request():
        """Execute before each request."""
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', str(time.time()))

    @app.after_request
    def after_request(response):
        """Execute after each request."""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            response.headers['X-Request-ID'] = g.request_id
            response.headers['X-Response-Time'] = str(elapsed)

            # Log request details
            logger.info(
                f'{request.method} {request.path} - '
                f'Status: {response.status_code} - '
                f'Duration: {elapsed:.3f}s - '
                f'Request-ID: {g.request_id}'
            )

        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        return response

    @app.teardown_request
    def teardown_request(exception=None):
        """Execute at the end of each request."""
        if exception:
            logger.error(f'Request error: {str(exception)}', exc_info=True)


class PerformanceMonitor:
    """Middleware for monitoring application performance."""

    def __init__(self, app=None):
        self.app = app
        self.slow_request_threshold = 1.0  # seconds

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with Flask app."""
        app.before_request(self.start_timer)
        app.after_request(self.log_request)

    def start_timer(self):
        """Start request timer."""
        g.start_time = time.time()

    def log_request(self, response):
        """Log request performance metrics."""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time

            if elapsed > self.slow_request_threshold:
                logger.warning(
                    f'Slow request detected: {request.method} {request.path} '
                    f'took {elapsed:.3f}s'
                )

        return response
