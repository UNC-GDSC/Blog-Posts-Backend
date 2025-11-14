"""Pytest configuration and fixtures."""
import pytest
from app import create_app
from app.models import db, Post


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app('testing')

    # Create tables
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_post(app):
    """Create a sample post for testing."""
    with app.app_context():
        post = Post(
            title="Test Post",
            content="This is a test post content."
        )
        db.session.add(post)
        db.session.commit()

        # Return the post ID
        post_id = post.id

    return post_id


@pytest.fixture
def multiple_posts(app):
    """Create multiple sample posts for testing."""
    with app.app_context():
        posts = [
            Post(title=f"Post {i}", content=f"Content for post {i}")
            for i in range(1, 16)
        ]
        db.session.add_all(posts)
        db.session.commit()

        post_ids = [post.id for post in posts]

    return post_ids
