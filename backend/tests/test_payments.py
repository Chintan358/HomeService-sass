"""Test suite for Payments & Invoicing module.

These tests cover creating a payment and checking its status.
Replace placeholder token and IDs with realistic values for your environment.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    return {"Authorization": "Bearer test-token"}

@pytest.fixture
def sample_payment_payload():
    return {
        "booking_id": 1,
        "amount": 5000,
        "currency": "INR",
        "method": "razorpay",
        # Additional fields as required by your API
    }

def test_create_payment(sample_payment_payload):
    response = client.post(
        "/payments/",
        json=sample_payment_payload,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert "payment_id" in data
    assert data["status"] == "pending" or data["status"] == "created"

def test_get_payment_status():
    # Assuming a payment_id of 1 exists; adjust as needed.
    response = client.get("/payments/1/status", headers=get_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
