# Contribs Project - Software Design Document

## 1. Project Overview
The Contribs project is a data transparency tool designed to track and visualize political contributions. It provides a mobile-friendly interface for citizens to explore where candidates receive their funding and which organizations or individuals are the primary contributors.

## 2. System Architecture
The system follows a classic client-server architecture with a containerized deployment strategy, utilizing a Zero Trust security model.

### 2.1 Backend (Django REST Framework)
The backend is a high-performance API service built with **Django 5.x** and **Django REST Framework (DRF)**.

- **Framework Stack:**
    - **Django 5.0+**: Core web framework.
    - **Django REST Framework**: For building the RESTful API.
    - **Gunicorn**: Production-grade WSGI HTTP Server.
    - **Whitenoise**: For efficient static file serving with Brotli compression.
    - **Psycopg2**: PostgreSQL database adapter.
- **Data Management:**
    - Custom management commands handle the ingestion of large legislative datasets.
    - Data is sourced from structured JSON files containing legislative and committee records.
- **API Features:**
    - **Pagination:** Global and per-view pagination for handling large contribution lists.
    - **Caching:** Optimized summary views to reduce database load on complex analytical queries.
    - **Environment Management:** Secured via standardized environment configuration files.

### 2.2 Frontend (Android / Kotlin)
The frontend is a native Android application built using modern reactive principles.

- **UI Framework:** **Jetpack Compose** with **Material 3** for a modern, responsive user interface.
- **Networking:** **Retrofit** with **OkHttpClient** and **GSON** for asynchronous API consumption.
- **Architecture Pattern:** **MVVM (Model-View-ViewModel)** to ensure clean separation of concerns and maintainable state.
- **Navigation:** **Compose Navigation** with a bottom bar for seamless transitions between Candidates, Committees, and Elections.
- **Image Loading:** **Coil** for efficient image fetching and caching.
- **Tools:** Android Studio with Kotlin and Gradle.

### 2.3 Infrastructure & Deployment
The project is hosted on Linux-based virtual private servers and managed via **Docker Compose**.

- **Security & Networking (Zero Trust):**
    - **Cloudflare Tunnels**: All inbound traffic is routed through secure, authenticated tunnels. No public ports are exposed on the host firewall.
    - **Isolated Networks:** Containers operate on private Docker networks to ensure service isolation.
- **Deployment Workflow:**
    - **Git-Based Deployment:** Automated via Git hooks.
    - **Server-Side Automation:** Scripts handle code checkout, Docker image builds, and service orchestration.
- **Container Services:**
    - **Web:** Django API server.
    - **DB:** PostgreSQL (Alpine) with health checks and persistent volume storage.
    - **Tunnel:** Cloudflare Tunnel agent.
    - **Wiki:** MkDocs Material for project documentation and landing page.
    - **Management:** Portainer (Docker management) and PGAdmin (Database GUI).
    - **Vaultwarden:** Bitwarden-compatible password manager for secure credential management.

## 3. Data Model
The database schema is designed for efficient querying of financial relationships:

- **Candidate:** Represents individuals running for office, including biographical data and affiliation.
- **Committee:** The financial entity through which funds flow to candidates.
- **Contribution:** Individual transactions linked to contributors, committees, and election cycles.
- **Election Summary:** Aggregated views of funding trends, providing high-level insights into political spending.

## 4. Operational Standards
- **Development Environment:** Local development uses container orchestration for the backend and Android Studio for the frontend.
- **Deployment:** Production deployments are triggered via version control pushes to dedicated remotes, which automate migrations and service restarts.
