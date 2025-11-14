"""Tag model module."""
from . import db

# Association table for many-to-many relationship between posts and tags
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=db.func.now())
)


class Tag(db.Model):
    """Tag model for categorizing posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Relationship to posts
    posts = db.relationship(
        'Post',
        secondary=post_tags,
        lazy='dynamic',
        backref=db.backref('tags', lazy='dynamic')
    )

    def __repr__(self):
        """String representation of Tag."""
        return f'<Tag {self.name}>'

    def to_dict(self):
        """Convert tag to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'post_count': self.posts.count()
        }

    @staticmethod
    def create_slug(name):
        """Create URL-friendly slug from name."""
        import re
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug

    @staticmethod
    def validate_tag_data(data):
        """
        Validate tag data.

        Args:
            data: Dictionary containing tag data

        Returns:
            tuple: (is_valid, error_message)
        """
        if not data:
            return False, "No data provided"

        if 'name' not in data or not data['name']:
            return False, "Tag name is required"

        if len(data['name']) > 50:
            return False, "Tag name must be 50 characters or less"

        if len(data['name'].strip()) == 0:
            return False, "Tag name cannot be empty or whitespace only"

        return True, None
