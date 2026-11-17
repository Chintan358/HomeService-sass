# backend/core/ratelimit.py
"""Rate limiting configuration using SlowAPI.
The ``limiter`` instance is attached to the FastAPI ``app`` in ``app/main.py``.
Default limit is generous (100/min) for most endpoints; sensitive routes (auth) use tighter limits.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Global limiter – can be overridden per‑router with ``@limiter.limit``
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
