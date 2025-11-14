"""Blog posts routes."""
from flask import Blueprint, request, jsonify
from app.models import db, Post
from app.utils import ValidationError, NotFoundError, paginate

posts_bp = Blueprint('posts', __name__, url_prefix='/api/v1/posts')


@posts_bp.route('', methods=['GET'])
def get_posts():
    """
    Get all posts with pagination, search, and filtering.

    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 10, max: 100)
        - search: Search term for title and content
        - sort: Sort field (created_at, updated_at, title)
        - order: Sort order (asc, desc)

    Returns:
        JSON response with paginated posts
    """
    # Build base query
    query = Post.query

    # Search functionality
    search_term = request.args.get('search', '').strip()
    if search_term:
        search_filter = f'%{search_term}%'
        query = query.filter(
            db.or_(
                Post.title.ilike(search_filter),
                Post.content.ilike(search_filter)
            )
        )

    # Sorting
    sort_field = request.args.get('sort', 'created_at')
    sort_order = request.args.get('order', 'desc')

    # Validate sort field
    valid_sort_fields = ['created_at', 'updated_at', 'title', 'id']
    if sort_field not in valid_sort_fields:
        sort_field = 'created_at'

    # Apply sorting
    sort_column = getattr(Post, sort_field)
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Paginate results
    result = paginate(query, endpoint='posts.get_posts')

    return jsonify(result), 200


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get a single post by ID.

    Args:
        post_id: Post ID

    Returns:
        JSON response with post data

    Raises:
        NotFoundError: If post not found
    """
    post = Post.query.get(post_id)
    if not post:
        raise NotFoundError(f"Post with ID {post_id} not found")

    return jsonify(post.to_dict()), 200


@posts_bp.route('', methods=['POST'])
def create_post():
    """
    Create a new post.

    Request Body:
        {
            "title": "Post title",
            "content": "Post content"
        }

    Returns:
        JSON response with created post

    Raises:
        ValidationError: If validation fails
    """
    data = request.get_json()

    # Validate data
    is_valid, error_message = Post.validate_post_data(data)
    if not is_valid:
        raise ValidationError(error_message)

    # Create new post
    new_post = Post(
        title=data['title'].strip(),
        content=data['content'].strip()
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201


@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing post.

    Args:
        post_id: Post ID

    Request Body:
        {
            "title": "Updated title",
            "content": "Updated content"
        }

    Returns:
        JSON response with updated post

    Raises:
        NotFoundError: If post not found
        ValidationError: If validation fails
    """
    post = Post.query.get(post_id)
    if not post:
        raise NotFoundError(f"Post with ID {post_id} not found")

    data = request.get_json()
    if not data:
        raise ValidationError("No data provided")

    # Update fields if provided
    if 'title' in data:
        if not data['title'] or len(data['title'].strip()) == 0:
            raise ValidationError("Title cannot be empty")
        if len(data['title']) > 150:
            raise ValidationError("Title must be 150 characters or less")
        post.title = data['title'].strip()

    if 'content' in data:
        if not data['content'] or len(data['content'].strip()) == 0:
            raise ValidationError("Content cannot be empty")
        post.content = data['content'].strip()

    db.session.commit()

    return jsonify(post.to_dict()), 200


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a post.

    Args:
        post_id: Post ID

    Returns:
        JSON response with success message

    Raises:
        NotFoundError: If post not found
    """
    post = Post.query.get(post_id)
    if not post:
        raise NotFoundError(f"Post with ID {post_id} not found")

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "message": "Post deleted successfully",
        "id": post_id
    }), 200
