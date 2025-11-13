"""Models package."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .post import Post

__all__ = ['db', 'migrate', 'Post']
