from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..routers import auth as auth_router
from ..routers import service_category as category_router
from ..routers import booking as booking_router
from ..routers import notification as notification_router
from ..routers import technician as technician_router
from ..routers import analytics as analytics_router
from ..core.ratelimit import limiter
from ..middleware.security_headers import SecurityHeadersMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI(title="Home Services Booking Backend", version="0.1.0")

# Attach limiter to app state
app.state.limiter = limiter

# Register exception handler for rate limit exceed
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# Add middlewares
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(category_router.router, prefix="/categories", tags=["service-categories"])
app.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])
app.include_router(technician_router.router, prefix="/technicians", tags=["technicians"])
app.include_router(notification_router.router, prefix="/notifications", tags=["notifications"])
app.include_router(analytics_router.router, prefix="/analytics", tags=["analytics"])

# Demo protected endpoint
from fastapi import Depends
from ..core.security import decode_access_token
from ..models.user import User
from ..utils.dependencies import get_current_user

@app.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}

app = FastAPI(title="Home Services Booking Backend", version="0.1.0")

# CORS (allow all for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(category_router.router, prefix="/categories", tags=["service-categories"])
app.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])
app.include_router(technician_router.router, prefix="/technicians", tags=["technicians"])
app.include_router(analytics_router.router, prefix="/analytics", tags=["analytics"])

# Demo protected endpoint
from fastapi import Depends, HTTPException, status
from ..core.security import decode_access_token
from ..core.config import settings
from ..models.user import User
from ..utils.dependencies import get_current_user

@app.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}
