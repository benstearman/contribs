# Contribs.app

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Website-contribs.app-indigo)](https://contribs.app)

**Empowering Financial Transparency in Politics.**

[Contribs.app](https://contribs.app) is a free, open-source political contributions **transparency engine** designed to pull back the curtain on election financing. By providing a modern, high-performance interface to complex legislative data, we empower citizens to see exactly where political influence is bought and sold.

## 🚀 Overview

Contribs aggregates and presents United States political contribution data from the Federal Election Commission (FEC). It offers a seamless, mobile-first experience for exploring funding trends, tracking individual donors, and analyzing the financial backing of political candidates.

### Key Features

- **Follow the Money:** Instantly track contributions from individual donors, corporate committees, and PACs directly to candidates.
- **Election Intelligence:** View aggregated summaries of funding trends across election cycles to understand the big picture.
- **Candidate Profiles:** Deep-dive into candidate-specific financial summaries, top contributors, and associated committees.
- **Privacy First:** No accounts, no sign-ups, and no tracking. Favorites are saved locally on your device.
- **Open-Source Integrity:** Built with transparency in mind, our code and data processing workflows are fully open for audit and improvement.

## 🛠️ Technology Stack

- **Frontend:** Android (Kotlin) utilizing **Jetpack Compose** for a modern, reactive UI.
- **Backend:** **Django** (Python) with **Django REST Framework** for a robust and scalable API.
- **Database:** **PostgreSQL** with GIN trigram indexes for high-performance searching across millions of records.
- **DevOps:** **Docker & Docker Compose** for containerization and isolated service management.
- **Deployment:** **Hetzner Cloud** with **Cloudflare Tunnels** for a secure, Zero Trust architecture.

## 📖 Documentation

- **[User Guide](landing/user-guide.md):** Detailed instructions on how to use the app, understand the data definitions, and explore the features.
- **[Architecture](landing/architecture.md):** Technical stack, system diagrams, and infrastructure overview.
- **[Design Document](landing/design.md):** Project overview, software design patterns, and data model definitions.

## 🚀 Getting Started

### Website & Landing Page
Visit [contribs.app](https://contribs.app) to learn more about the project and view the latest screenshots.

### Android Application
Download the latest prototype directly from the [GitHub Releases](https://github.com/benstearman/contribs/releases/latest) page.

## 🤝 Contributing

We welcome contributions, bug reports, and feature requests! As an open-source project, we value community input to help make political finance data more accessible to everyone.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

*Contribs.app is a non-partisan project dedicated to open data and democratic accountability.*
