"""Test suite for Analytics Dashboards module.

Provides basic checks for admin, provider, and customer analytics endpoints.
Replace auth token as appropriate.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    return {"Authorization": "Bearer test-token"}

def test_admin_analytics():
    response = client.get("/analytics/admin", headers=get_auth_headers())
    assert response.status_code == 200
    data = response.json()
    # Expect certain keys; adjust based on actual schema.
    assert isinstance(data, dict)

def test_provider_analytics():
    response = client.get("/analytics/provider", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_customer_analytics():
    response = client.get("/analytics/customer", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
