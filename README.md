# Linux/macOS: source .venv/bin/activate

A synthetic-data prototype for surplus forecasting, inventory reservations and human-reviewed redistribution workflows.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Architecture](<docs/assets/02-system-architecture.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Existing published preview link: [Open browser preview](https://harshakavali81-collab.github.io/harshavardhan-portfolio/). This update does not independently verify its availability or backend deployment.

## Key Features

A portfolio-ready local application for understanding possible food surplus, recording actually available inventory, screening potential recipient organizations, reserving stock safely, and tracking confirmations separately from forecasts and reservations.

| Area | Demonstration |
|---|---|
| Dashboard | Available, reserved, confirmed-collected kilograms + synthetic trends |
| Donor inventory | Items, quantities, allergens, storage, pickup deadlines and donor safety acknowledgment |
| Recipients | Demo capacity, category, cold-chain compatibility, distance and separate demo-only verification; API users cannot self-verify |
| Smart matching | Rule-based hard gates with candidate ranking by approximate proximity |
| Donation tracking | Atomic inventory allocation, recipient capacity locks, cancellation and explicit confirmation |
| ML & analytics | Time-aware random forest vs seasonal-naive baseline; synthetic dataset and Power BI guide |
| Engineering | API docs, 52 passing Python tests plus 3 PostgreSQL integration checks, Docker, GitHub Actions, 10 original SVG assets |

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution.git
cd FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution
```

```bash
cp .env.example .env
docker compose up --build
```
Frontend: **http://localhost:3000** · API: **http://localhost:8000/docs**. The Compose services bind to localhost intentionally.

## Challenges & Solutions

**Repository organization:** this project uses `src/`, `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

<div align="center">
<img src="docs/assets/01-hero-banner.svg" width="100%" alt="FoodBridge AI — Food surplus forecasting and community redistribution">

<p><strong>Food Waste Prediction & Community Redistribution</strong></p>
<p>Data science · FastAPI · SQLAlchemy · React · Recharts · Scikit-learn · Docker</p>
<p><img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python"><img alt="Synthetic demo" src="https://img.shields.io/badge/Data-SYNTHETIC-important"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-green"></p>
</div>

> [!IMPORTANT]
> **Educational portfolio prototype, not a live food donation service.** Sample partners and historical records are fictional. No real food is being supplied, no food-safety determination is automated and no avoided-waste / meals-served impact is independently verified. Predictions are not physical inventory; any donation requires authorized human review and confirmation.

[](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/workflows/ci.yml)

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `powerbi/` | Power BI build assets |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

See [LICENSE](LICENSE) for the existing terms.
