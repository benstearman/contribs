# Technical Architecture

This document provides a visual representation and overview of the technical stack for the Contribs project.

## System Architecture Diagram

```mermaid
graph TD
    subgraph Client_Side [Frontend - Android App]
        A[Jetpack Compose UI] --> B[MVVM ViewModel]
        B --> C[Retrofit / OkHttp]
    end

    subgraph Security_Layer [Zero Trust Access]
        C -- HTTPS via Tunnel --> D[Cloudflare Edge]
        D -- Authenticated Tunnel --> E[Cloudflare Tunnel Agent]
    end

    subgraph Server_Side [Docker Compose Stack]
        E --> F[Gunicorn / Django API]
        F --> G[(PostgreSQL)]
        F --> H[Whitenoise Static Serving]
    end

    subgraph Infrastructure [Linux VPS Hosting]
        F & G & E -.-> I[Isolated Docker Network]
        G -.-> J[Persistent Volumes]
    end

    classDef tech fill:#f9f,stroke:#333,stroke-width:2px;
    class A,F,G,E tech;
```

## Technical Stack Details

### Backend
- **Framework:** Django 5.x / Django REST Framework
- **Server:** Gunicorn with WhiteNoise
- **Database:** PostgreSQL (Alpine)

### Frontend
- **Framework:** Jetpack Compose (Kotlin)
- **Architecture:** MVVM
- **Networking:** Retrofit / OkHttp

### Infrastructure & Security
- **Hosting:** Hetzner Cloud (Ubuntu 24.04 LTS)
- **Containerization:** Docker Compose
- **Security:** Cloudflare Tunnels (Zero Trust)
