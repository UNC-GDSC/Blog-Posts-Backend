"""Tests for post routes."""
import json
import pytest


class TestGetPosts:
    """Tests for GET /api/v1/posts endpoint."""

    def test_get_posts_empty(self, client):
        """Test getting posts when database is empty."""
        response = client.get('/api/v1/posts')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'items' in data
        assert len(data['items']) == 0
        assert 'meta' in data

    def test_get_posts(self, client, multiple_posts):
        """Test getting posts with pagination."""
        response = client.get('/api/v1/posts')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'items' in data
        assert len(data['items']) == 10  # Default per_page
        assert 'meta' in data
        assert data['meta']['total_items'] == 15
        assert data['meta']['total_pages'] == 2

    def test_get_posts_pagination(self, client, multiple_posts):
        """Test pagination parameters."""
        response = client.get('/api/v1/posts?page=2&per_page=5')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data['items']) == 5
        assert data['meta']['page'] == 2
        assert data['meta']['per_page'] == 5

    def test_get_posts_search(self, client, multiple_posts):
        """Test search functionality."""
        response = client.get('/api/v1/posts?search=Post 1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data['items']) > 0
        # Should match "Post 1", "Post 10", "Post 11", etc.

    def test_get_posts_sort(self, client, multiple_posts):
        """Test sorting functionality."""
        response = client.get('/api/v1/posts?sort=title&order=asc')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data['items']) > 0


class TestGetPost:
    """Tests for GET /api/v1/posts/<id> endpoint."""

    def test_get_post_success(self, client, sample_post):
        """Test getting a single post."""
        response = client.get(f'/api/v1/posts/{sample_post}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == sample_post
        assert data['title'] == "Test Post"
        assert data['content'] == "This is a test post content."

    def test_get_post_not_found(self, client):
        """Test getting a non-existent post."""
        response = client.get('/api/v1/posts/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert 'error' in data


class TestCreatePost:
    """Tests for POST /api/v1/posts endpoint."""

    def test_create_post_success(self, client):
        """Test creating a post successfully."""
        post_data = {
            'title': 'New Post',
            'content': 'This is a new post.'
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['title'] == post_data['title']
        assert data['content'] == post_data['content']
        assert 'id' in data
        assert 'created_at' in data

    def test_create_post_missing_title(self, client):
        """Test creating a post without title."""
        post_data = {
            'content': 'This is a new post.'
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_post_missing_content(self, client):
        """Test creating a post without content."""
        post_data = {
            'title': 'New Post'
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_post_empty_title(self, client):
        """Test creating a post with empty title."""
        post_data = {
            'title': '',
            'content': 'Content here'
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_post_title_too_long(self, client):
        """Test creating a post with title exceeding max length."""
        post_data = {
            'title': 'x' * 151,
            'content': 'Content here'
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        assert response.status_code == 400


class TestUpdatePost:
    """Tests for PUT /api/v1/posts/<id> endpoint."""

    def test_update_post_success(self, client, sample_post):
        """Test updating a post successfully."""
        update_data = {
            'title': 'Updated Title',
            'content': 'Updated content.'
        }
        response = client.put(
            f'/api/v1/posts/{sample_post}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['content'] == update_data['content']

    def test_update_post_partial(self, client, sample_post):
        """Test partial update of a post."""
        update_data = {
            'title': 'Updated Title Only'
        }
        response = client.put(
            f'/api/v1/posts/{sample_post}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['title'] == update_data['title']

    def test_update_post_not_found(self, client):
        """Test updating a non-existent post."""
        update_data = {
            'title': 'Updated Title'
        }
        response = client.put(
            '/api/v1/posts/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_update_post_empty_title(self, client, sample_post):
        """Test updating with empty title."""
        update_data = {
            'title': ''
        }
        response = client.put(
            f'/api/v1/posts/{sample_post}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 400


class TestDeletePost:
    """Tests for DELETE /api/v1/posts/<id> endpoint."""

    def test_delete_post_success(self, client, sample_post):
        """Test deleting a post successfully."""
        response = client.delete(f'/api/v1/posts/{sample_post}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'message' in data

        # Verify post is deleted
        response = client.get(f'/api/v1/posts/{sample_post}')
        assert response.status_code == 404

    def test_delete_post_not_found(self, client):
        """Test deleting a non-existent post."""
        response = client.delete('/api/v1/posts/999')
        assert response.status_code == 404
