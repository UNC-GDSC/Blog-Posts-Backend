"""Application factory module."""
import logging
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from app.config import get_config
from app.models import db, migrate
from app.routes import posts_bp, health_bp
from app.utils.errors import register_error_handlers


def create_app(config_name=None):
    """
    Application factory function.

    Args:
        config_name: Configuration name (development, testing, production)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Initialize Swagger documentation
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }

    swagger_template = {
        "info": {
            "title": "Blog Posts API",
            "description": "RESTful API for managing blog posts",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
            }
        },
        "schemes": ["http", "https"],
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Register blueprints
    app.register_blueprint(posts_bp)
    app.register_blueprint(health_bp)

    # Register error handlers
    register_error_handlers(app)

    # Configure logging
    configure_logging(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


def configure_logging(app):
    """
    Configure application logging.

    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        # Configure logging for production
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        app.logger.setLevel(logging.INFO)
        app.logger.info('Blog API startup')
    else:
        # Configure logging for development
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        app.logger.setLevel(logging.DEBUG)
