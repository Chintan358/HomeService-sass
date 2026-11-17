# Presentation – Home Services Booking SaaS

Below is a **Markdown carousel** you can paste into any slide‑generation tool (e.g., remark, reveal.js) or convert to PDF. Each slide is separated by `<!-- slide -->`.

````carousel
## Slide 1 – Project Overview
- **Goal**: Build a full‑stack SaaS for home‑service booking (customers ↔ providers ↔ technicians).
- **Tech Stack**  
  - Frontend: React + Vite + Tailwind CSS  
  - Backend: FastAPI + SQLAlchemy + MySQL (SQLite for dev)  
  - Auth: JWT + RBAC  
  - Payments: Razorpay (test mode)  
  - Media: Cloudinary  
  - CI/CD: GitHub Actions → Vercel (frontend) + Render (backend)

<!-- slide -->
## Slide 2 – Architecture Diagram
```mermaid
flowchart LR
    subgraph Frontend[React Frontend (Tailwind, Vite)]
        UI[UI Components & Pages]
        AuthHook[Auth Hook (JWT)]
        API[API Service Layer]
    end
    subgraph Backend[FastAPI Backend (Python, SQLAlchemy)]
        AuthAPI[Auth Endpoints]
        CategoryAPI[Service Category CRUD]
        BookingAPI[Booking & Scheduler]
        PaymentAPI[Payment & Invoice]
        TechAPI[Technician Management]
        NotifyAPI[Notification Service]
        AnalyticsAPI[Analytics & Reports]
        DB[(MySQL + SQLAlchemy)]
    end
    DB <-.-> Backend
    Cloud[Cloudinary]
    Pay[Razorpay Test]
    UI --> API --> AuthHook
    API --> AuthAPI
    API --> CategoryAPI
    API --> BookingAPI
    API --> TechAPI
    API --> PaymentAPI
    API --> NotifyAPI
    API --> AnalyticsAPI
    PaymentAPI --> Pay
    NotifyAPI --> DB
    AnalyticsAPI --> DB
    API --> Cloud
```
```

<!-- slide -->
## Slide 3 – Core Features (User Stories)
| Role | Primary Actions |
|------|-----------------|
| **Customer** | Register → Browse services → Book → Pay → Rate/Review |
| **Service Provider** | Register → Manage services → Accept bookings → Assign technicians |
| **Technician** | View assigned jobs → Update status → Upload completion images |
| **Super Admin** | Verify providers → Manage categories → View analytics → Issue coupons |

<!-- slide -->
## Slide 4 – Security Hardening
- **Rate Limiting** – 100 req/min globally, tighter limits on auth endpoints (SlowAPI).  
- **Security Headers** – CSP, HSTS, X‑Frame‑Options, X‑Content‑Type‑Options, Referrer‑Policy.  
- **Password Hashing** – `passlib` + bcrypt.  
- **RBAC** – All routes guarded by JWT + role checks.  
- **OWASP Checklist** – Covered in the Security module.

<!-- slide -->
## Slide 5 – CI / CD Pipeline
1. **GitHub Actions** – lint, format, unit & integration tests.  
2. **Frontend** – `npm run build` → Vercel (`vercel --prod`).  
3. **Backend** – Docker build → push to Docker Hub → Render redeploy via Deploy Hook.  
4. **Automatic Rollback** – Failed workflow aborts deployment; Render keeps the previous container alive.

<!-- slide -->
## Slide 6 – Demo Screens (placeholders)
> _Replace these screenshots with actual UI shots after the first live deployment._

![Landing page](/absolute/path/to/placeholder/landing.png)
<!-- slide -->
![Customer Dashboard](/absolute/path/to/placeholder/customer_dashboard.png)
<!-- slide -->
![Provider Booking List](/absolute/path/to/placeholder/provider_bookings.png)

<!-- slide -->
## Slide 7 – Analytics Highlights
- **Admin**: Total revenue, commission, monthly bookings chart.  
- **Provider**: Daily earnings, average rating, month‑over‑month growth.  
- **Customer**: Upcoming appointments, pending payments, status breakdown.

<!-- slide -->
## Slide 8 – Next Steps & Roadmap
- **Production Hardening** – Monitoring (Sentry), autoscaling, CDN for static assets.  
- **Feature Extensions** – Real‑time chat, calendar sync, multi‑language support.  
- **User Acceptance Testing** – Gather feedback from pilot users.

---

*End of presentation.*
```