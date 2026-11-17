```mermaid
flowchart LR
    subgraph Frontend[React Frontend (Tailwind, Vite)]
        UI[UI Components & Pages]
        AuthHook[Auth Hook (JWT)]
        API[API Service Layer]
    end
    subgraph Backend[FastAPI Backend (Python, SQLAlchemy)]
        AuthAPI[Auth Endpoints]
        UserAPI[User & Role Management]
        CategoryAPI[Service Category CRUD]
        BookingAPI[Booking & Scheduler]
        PaymentAPI[Payment & Invoice]
        TechAPI[Technician Management]
        NotifyAPI[Notification Service]
        AnalyticsAPI[Analytics & Reports]
        FileAPI[Cloudinary Upload]
        DB[(MySQL + SQLAlchemy)]
    end
    DB <-.-> Backend
    Cloud[Cloudinary]
    Pay[Razorpay Test]
    
    UI --> API --> AuthHook
    API --> AuthAPI
    API --> UserAPI
    API --> CategoryAPI
    API --> BookingAPI
    API --> TechAPI
    API --> PaymentAPI
    API --> NotifyAPI
    API --> AnalyticsAPI
    API --> FileAPI
    AuthAPI --> DB
    UserAPI --> DB
    CategoryAPI --> DB
    BookingAPI --> DB
    TechAPI --> DB
    PaymentAPI --> DB
    NotifyAPI --> DB
    AnalyticsAPI --> DB
    FileAPI --> Cloud
    PaymentAPI --> Pay
```
