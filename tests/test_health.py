"""Tests for health check routes."""
import json


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'status' in data
    assert 'database' in data
    assert 'api' in data
    assert data['api'] == 'healthy'


def test_ping(client):
    """Test the ping endpoint."""
    response = client.get('/ping')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['message'] == 'pong'
