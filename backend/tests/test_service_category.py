import pytest
from httpx import AsyncClient
from backend.core.database import Base, get_db
from backend.core.config import settings
from backend.app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Override DB for tests (SQLite)
TEST_DATABASE_URL = "sqlite:///./test_service.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_service_category_crud():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Register a superadmin
        reg_payload = {"email": "admin@example.com", "password": "adminpass", "role": "superadmin"}
        r = await ac.post("/auth/register", json=reg_payload)
        assert r.status_code == 201
        token_admin = r.json()["access_token"]
        headers_admin = {"Authorization": f"Bearer {token_admin}"}

        # Create a category
        cat_payload = {"name": "Plumbing", "description": "All plumbing services", "image_url": None}
        r = await ac.post("/categories/", json=cat_payload, headers=headers_admin)
        assert r.status_code == 201
        cat = r.json()
        assert cat["name"] == "Plumbing"
        cat_id = cat["id"]

        # Get the category
        r = await ac.get(f"/categories/{cat_id}")
        assert r.status_code == 200
        assert r.json()["name"] == "Plumbing"

        # Update the category (change description)
        update_payload = {"description": "Updated description"}
        r = await ac.put(f"/categories/{cat_id}", json=update_payload, headers=headers_admin)
        assert r.status_code == 200
        assert r.json()["description"] == "Updated description"

        # List categories
        r = await ac.get("/categories/")
        assert r.status_code == 200
        assert len(r.json()) >= 1

        # Delete the category
        r = await ac.delete(f"/categories/{cat_id}", headers=headers_admin)
        assert r.status_code == 204
        # Verify deletion
        r = await ac.get(f"/categories/{cat_id}")
        assert r.status_code == 404
