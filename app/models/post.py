"""Post model module."""
from datetime import datetime
from . import db


class Post(db.Model):
    """Blog post model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        """String representation of Post."""
        return f'<Post {self.id}: {self.title}>'

    def to_dict(self):
        """Convert post to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def validate_post_data(data):
        """
        Validate post data.

        Args:
            data: Dictionary containing post data

        Returns:
            tuple: (is_valid, error_message)
        """
        if not data:
            return False, "No data provided"

        if 'title' not in data or not data['title']:
            return False, "Title is required"

        if 'content' not in data or not data['content']:
            return False, "Content is required"

        if len(data['title']) > 150:
            return False, "Title must be 150 characters or less"

        if len(data['title'].strip()) == 0:
            return False, "Title cannot be empty or whitespace only"

        if len(data['content'].strip()) == 0:
            return False, "Content cannot be empty or whitespace only"

        return True, None
