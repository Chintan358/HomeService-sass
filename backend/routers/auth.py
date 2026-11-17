"""Authentication router for FastAPI backend.
Provides registration and login endpoints that return JWT access tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_password_hash, verify_password, create_access_token
from ..models.user import User
from ..schemas.auth import RegisterIn, LoginIn, TokenOut

router = APIRouter()

@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterIn,
    db: Session = Depends(get_db),
):
    # Ensure email is not already taken
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(payload.password)
    user = User(email=payload.email, hashed_password=hashed, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token({"sub": user.id, "role": user.role.value})
    return TokenOut(access_token=access_token, token_type="bearer")

@router.post("/login", response_model=TokenOut)
def login(
    payload: LoginIn,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token({"sub": user.id, "role": user.role.value})
    return TokenOut(access_token=access_token, token_type="bearer")
