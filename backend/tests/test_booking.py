"""Test suite for Booking module.

These tests verify the basic CRUD operations for bookings.
The actual authentication/authorization is assumed to be handled by a test fixture or mock token.
Replace the placeholder data and token with real values as needed.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper to obtain an auth token (placeholder) – adjust according to your auth implementation.
def get_auth_headers():
    # TODO: Replace with a real token acquisition, e.g., login request.
    return {"Authorization": "Bearer test-token"}

@pytest.fixture
def sample_booking_payload():
    return {
        "service_category_id": 1,
        "customer_id": 1,
        "scheduled_time": "2023-12-01T10:00:00Z",
        "notes": "Test booking"
    }

def test_create_booking(sample_booking_payload):
    response = client.post(
        "/bookings/",
        json=sample_booking_payload,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert "id" in data
    assert data["service_category_id"] == sample_booking_payload["service_category_id"]

def test_get_bookings_list():
    response = client.get("/bookings/", headers=get_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
