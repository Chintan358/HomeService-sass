import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file if present
dotenv_path = BASE_DIR / ".." / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    # fallback to .env in project root
    load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    # Add more settings as needed

settings = Settings()
