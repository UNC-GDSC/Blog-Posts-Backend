"""Pagination utilities."""
from flask import request, url_for


def paginate(query, endpoint='posts.get_posts'):
    """
    Paginate SQLAlchemy query results.

    Args:
        query: SQLAlchemy query object
        endpoint: Flask endpoint for generating pagination links

    Returns:
        dict: Paginated results with metadata
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Limit per_page to prevent abuse
    per_page = min(per_page, 100)

    # Get paginated results
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Build response
    result = {
        'items': [item.to_dict() for item in pagination.items],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        }
    }

    # Add pagination links
    if pagination.has_next:
        result['meta']['next_page'] = url_for(
            endpoint,
            page=page + 1,
            per_page=per_page,
            _external=True
        )

    if pagination.has_prev:
        result['meta']['prev_page'] = url_for(
            endpoint,
            page=page - 1,
            per_page=per_page,
            _external=True
        )

    return result
