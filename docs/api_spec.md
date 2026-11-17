# API Specification

The FastAPI application automatically generates an OpenAPI specification at **`/openapi.json`** and an interactive Swagger UI at **`/docs`**.

For reference, the relevant sections of the API are summarized below.

---

## Authentication (`/auth`)
| Method | Endpoint | Description | Request Schema | Response Schema |
|--------|----------|-------------|----------------|-----------------|
| `POST` | `/auth/register` | Register a new user (any role). | `RegisterIn` | `TokenOut` |
| `POST` | `/auth/login` | Login and obtain JWT. | `LoginIn` | `TokenOut` |

---

## Service Categories (`/categories`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/categories/` | Create a new category (superadmin). |
| `GET` | `/categories/` | List all categories |
| `GET` | `/categories/{id}` | Get a single category |
| `PUT` | `/categories/{id}` | Update a category (superadmin) |
| `DELETE` | `/categories/{id}` | Delete a category (superadmin) |

---

## Bookings (`/bookings`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/bookings/` | Customer creates a booking (double‑booking guard). |
| `GET` | `/bookings/` | List bookings (role‑scoped). |
| `GET` | `/bookings/{id}` | Retrieve a booking (owner/provider/superadmin). |
| `PUT` | `/bookings/{id}/status` | Provider updates status. |
| `DELETE` | `/bookings/{id}` | Customer or superadmin cancels. |

---

## Payments (`/payments`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/payments/` | Create a payment record (customer). |
| `GET` | `/payments/{id}` | Retrieve payment (owner/provider/superadmin). |
| `PUT` | `/payments/{id}/status` | Provider or superadmin updates status. |
| `GET` | `/payments/{id}/invoice` | Generate PDF invoice. |

---

## Technicians (`/technicians`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/technicians/` | Provider creates a technician. |
| `GET` | `/technicians/` | Superadmin lists all technicians. |
| `GET` | `/technicians/{id}` | Get technician details (owner/provider/superadmin). |
| `PUT` | `/technicians/{id}` | Provider updates. |
| `DELETE` | `/technicians/{id}` | Superadmin deletes. |

---

## Notifications (`/notifications`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/notifications/` | Superadmin creates a notification for a user. |
| `GET` | `/notifications/user/{user_id}` | List a user’s notifications (owner/superadmin). |
| `PATCH` | `/notifications/{notif_id}/read` | Mark as read/unread (owner/superadmin). |
| `DELETE` | `/notifications/{notif_id}` | Delete (superadmin). |

---

## Analytics (`/analytics`)
| Endpoint | Description |
|----------|-------------|
| `GET /analytics/admin` | Admin‑level summary statistics. |
| `GET /analytics/provider` | Provider‑specific dashboard data. |
| `GET /analytics/customer` | Customer‑focused dashboard data. |

---

## Security & Rate Limiting
All endpoints are protected by JWT authentication and role‑based access control. Sensitive routes (e.g., `/auth/login`) have tighter rate‑limit decorators such as `@limiter.limit("10/minute")`. The global limiter is configured in `backend/core/ratelimit.py`.

---

**Full OpenAPI spec** can be downloaded from the running server:
```
GET http://<host>:8000/openapi.json
```