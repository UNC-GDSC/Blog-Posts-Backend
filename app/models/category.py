"""Category model module."""
from . import db


class Category(db.Model):
    """Category model for organizing posts."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Self-referential relationship for hierarchical categories
    children = db.relationship(
        'Category',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic'
    )

    # Relationship to posts
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        """String representation of Category."""
        return f'<Category {self.name}>'

    def to_dict(self, include_children=False):
        """Convert category to dictionary for JSON serialization."""
        result = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat(),
            'post_count': self.posts.count()
        }

        if include_children:
            result['children'] = [child.to_dict() for child in self.children]

        return result

    @staticmethod
    def create_slug(name):
        """Create URL-friendly slug from name."""
        import re
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug

    @staticmethod
    def validate_category_data(data):
        """
        Validate category data.

        Args:
            data: Dictionary containing category data

        Returns:
            tuple: (is_valid, error_message)
        """
        if not data:
            return False, "No data provided"

        if 'name' not in data or not data['name']:
            return False, "Category name is required"

        if len(data['name']) > 100:
            return False, "Category name must be 100 characters or less"

        if len(data['name'].strip()) == 0:
            return False, "Category name cannot be empty or whitespace only"

        return True, None
