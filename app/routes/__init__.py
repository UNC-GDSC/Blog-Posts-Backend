"""Routes package."""
from .posts import posts_bp
from .health import health_bp

__all__ = ['posts_bp', 'health_bp']
