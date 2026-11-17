import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base, get_db
from backend.core.config import settings
from backend.app.main import app

# Use a separate SQLite DB for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Register a new user
        register_payload = {
            "email": "test@example.com",
            "password": "strongpassword",
            "role": "customer"
        }
        r = await ac.post("/auth/register", json=register_payload)
        assert r.status_code == 201
        token_data = r.json()
        assert "access_token" in token_data
        access_token = token_data["access_token"]

        # Login with same credentials
        login_payload = {"email": "test@example.com", "password": "strongpassword"}
        r = await ac.post("/auth/login", json=login_payload)
        assert r.status_code == 200
        login_data = r.json()
        assert login_data["access_token"] == access_token

        # Access protected endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        r = await ac.get("/me", headers=headers)
        assert r.status_code == 200
        user_info = r.json()
        assert user_info["email"] == "test@example.com"
        assert user_info["role"] == "customer"
