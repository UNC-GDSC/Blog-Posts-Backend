"""Post model module."""
from datetime import datetime
from . import db


class Post(db.Model):
    """Blog post model."""

    __tablename__ = 'posts'
    __table_args__ = (
        db.Index('idx_post_created_at', 'created_at'),
        db.Index('idx_post_title', 'title'),
        db.Index('idx_post_category', 'category_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    is_published = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        """String representation of Post."""
        return f'<Post {self.id}: {self.title}>'

    def to_dict(self, include_tags=True):
        """Convert post to dictionary for JSON serialization."""
        result = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if self.category:
            result['category'] = {
                'id': self.category.id,
                'name': self.category.name,
                'slug': self.category.slug
            }

        if include_tags:
            result['tags'] = [
                {'id': tag.id, 'name': tag.name, 'slug': tag.slug}
                for tag in self.tags.all()
            ]

        return result

    def soft_delete(self):
        """Soft delete the post."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restore a soft-deleted post."""
        self.is_deleted = False
        self.deleted_at = None

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
