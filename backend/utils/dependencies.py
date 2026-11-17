"""Utility dependencies for FastAPI routes.
Provides a reusable ``get_current_user`` dependency that extracts the JWT token
from the ``Authorization: Bearer <token>`` header, validates it, and returns the
SQLAlchemy ``User`` instance.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..core.security import decode_access_token
from ..core.database import get_db
from ..models.user import User

# Security scheme – FastAPI will look for the ``Authorization`` header.
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Validate JWT and fetch the corresponding ``User``.

    Args:
        credentials: Provided by ``HTTPBearer`` – contains the raw token.
        db: Database session from ``get_db``.
    Returns:
        The authenticated ``User`` object.
    Raises:
        HTTPException 401 – if token is missing, malformed or user not found.
    """
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation error",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return user
