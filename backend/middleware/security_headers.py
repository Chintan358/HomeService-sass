# backend/middleware/security_headers.py
"""Middleware to add common security headers to all responses.
Inspired by Helmet (Node.js) – helps mitigate XSS, MIME‑type sniffing, click‑jacking, and enforces HTTPS (HSTS).
"""

from starlette.types import ASGIApp, Message, Receive, Scope, Send

class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        async def send_wrapper(message: Message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                # Helper to add a header (bytes key/value)
                def add(name: str, value: str):
                    headers.append((name.encode("latin-1"), value.encode("latin-1")))

                # Prevent MIME type sniffing
                add("X-Content-Type-Options", "nosniff")
                # Click‑jacking protection
                add("X-Frame-Options", "DENY")
                # XSS protection (basic)
                add("X-XSS-Protection", "1; mode=block")
                # HSTS – enforce HTTPS (max‑age 6 months, include subdomains)
                add("Strict-Transport-Security", "max-age=15768000; includeSubDomains; preload")
                # Referrer‑Policy – no referrer info sent to external sites
                add("Referrer-Policy", "no-referrer")
                # Content Security Policy – very restrictive default (adjust per UI needs)
                add(
                    "Content-Security-Policy",
                    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;",
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)
