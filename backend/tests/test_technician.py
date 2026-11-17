"""Test suite for Technician module.

Basic CRUD tests for technician management.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    return {"Authorization": "Bearer test-token"}

@pytest.fixture
def sample_technician_payload():
    return {
        "name": "John Doe",
        "expertise": "Plumbing",
        "available": True
    }

def test_create_technician(sample_technician_payload):
    response = client.post(
        "/technicians/",
        json=sample_technician_payload,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert "id" in data
    assert data["name"] == sample_technician_payload["name"]

def test_list_technicians():
    response = client.get("/technicians/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)
