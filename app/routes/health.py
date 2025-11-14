"""Health check routes."""
from flask import Blueprint, jsonify
from app.models import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON response with health status
    """
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'

    status = {
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'database': db_status,
        'api': 'healthy'
    }

    status_code = 200 if status['status'] == 'healthy' else 503

    return jsonify(status), status_code


@health_bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple ping endpoint.

    Returns:
        JSON response with pong
    """
    return jsonify({'message': 'pong'}), 200
