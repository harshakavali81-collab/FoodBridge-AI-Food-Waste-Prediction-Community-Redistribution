<div align="center">
<img src="docs/assets/01-hero-banner.svg" width="100%" alt="FoodBridge AI — Food surplus forecasting and community redistribution">
<h1>🌱 FoodBridge AI</h1>
<p><strong>Food Waste Prediction & Community Redistribution</strong></p>
<p>Data science · FastAPI · SQLAlchemy · React · Recharts · Scikit-learn · Docker</p>
<p><img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python"><img alt="Synthetic demo" src="https://img.shields.io/badge/Data-SYNTHETIC-important"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-green"></p>
</div>

> [!IMPORTANT]
> **Educational portfolio prototype, not a live food donation service.** Sample partners and historical records are fictional. No real food is being supplied, no food-safety determination is automated and no avoided-waste / meals-served impact is independently verified. Predictions are not physical inventory; any donation requires authorized human review and confirmation.

[![CI](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/workflows/ci.yml/badge.svg)](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/workflows/ci.yml)

## What is FoodBridge AI?
A portfolio-ready local application for understanding possible food surplus, recording actually available inventory, screening potential recipient organizations, reserving stock safely, and tracking confirmations separately from forecasts and reservations.

| Area | Demonstration |
|---|---|
| Dashboard | Available, reserved, confirmed-collected kilograms + synthetic trends |
| Donor inventory | Items, quantities, allergens, storage, pickup deadlines and donor safety acknowledgment |
| Recipients | Demo capacity, category, cold-chain compatibility, distance and separate demo-only verification; API users cannot self-verify |
| Smart matching | Rule-based hard gates with candidate ranking by approximate proximity |
| Donation tracking | Atomic inventory allocation, recipient capacity locks, cancellation and explicit confirmation |
| ML & analytics | Time-aware random forest vs seasonal-naive baseline; synthetic dataset and Power BI guide |
| Engineering | API docs, 34 passing automated tests, Docker, GitHub Actions, 10 original SVG assets |

## Visual project tour — 10 original diagrams & charts

| System architecture | Donation lifecycle |
|---|---|
| ![Architecture](docs/assets/02-system-architecture.svg) | ![Workflow](docs/assets/03-redistribution-workflow.svg) |
| Eligibility decision tree | Machine-learning pipeline |
| ![Matching](docs/assets/04-matching-decision-tree.svg) | ![Forecasting](docs/assets/05-forecasting-pipeline.svg) |
| Research and operations lineage | Model comparison (illustrative example) |
| ![Lineage](docs/assets/06-data-lineage.svg) | ![Comparison](docs/assets/07-model-comparison.svg) |
| Synthetic time-series | Synthetic category mix |
| ![Trends](docs/assets/08-surplus-trends.svg) | ![Mix](docs/assets/09-category-mix.svg) |
| Responsible impact accounting | Banner |
| ![Funnel](docs/assets/10-impact-funnel.svg) | ![Banner](docs/assets/01-hero-banner.svg) |

The model comparison image rounds the verified synthetic-data evaluation (Random Forest 3.908 kg MAE versus lag-7 baseline 5.49 kg MAE); these figures do not generalize to live food operations. These pictures are illustrations, not verified real-world donations.

## Run locally — Docker (recommended)
```bash
cp .env.example .env
docker compose up --build
```
Frontend: **http://localhost:3000** · API: **http://localhost:8000/docs**. The Compose services bind to localhost intentionally.

## Run manually
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_synthetic.py
PYTHONPATH=.:src uvicorn backend.app.main:app --reload --port 8000
```
For PowerShell, set `$env:PYTHONPATH='.;src'` and then run `uvicorn backend.app.main:app --reload --port 8000`.

Second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open **http://localhost:5173**. Requirements: Python 3.12+, Node 22+.

## Train and evaluate
```bash
PYTHONPATH=.:src python -m foodbridge.forecasting.train --data data/synthetic/daily_operations.csv --output models
cat models/evaluation.json
PYTHONPATH=.:src python -m pytest -q
```

**Method:** Past-only lag-1, lag-7 and 7-day rolling historical surplus; chronological 80/20 date split; Random Forest vs lag-7 baseline; report MAE, RMSE and WAPE. Test lag features require observed history, so this is an offline one-step-ahead evaluation, **not** a real multi-day autonomous forecast. API forecast preview is explicitly a 7-day moving-average baseline.

## Architecture
```mermaid
flowchart LR
 D[Donor and recipient dashboard] --> API[FastAPI + validation]
 API --> DB[(SQLAlchemy DB)]
 API --> RULES[Hard-gated recipient eligibility]
 RULES --> DB
 CSV[Synthetic operations] --> ETL[Validated ETL and past-only features]
 ETL --> ML[Chronological ML evaluation]
 ETL --> BI[Recharts and Power BI]
 PUB[FAO published studies] --> RESEARCH[Separate research files]
```

## Project structure
```text
FoodBridge AI/
├── backend/app/          FastAPI, schemas, SQLAlchemy models & four route modules
├── frontend/src/         React dashboard, six pages, matching and donation forms
├── src/foodbridge/       Ingestion, processing, forecasting, matching, monitoring
├── data/synthetic/       840-row reproducible synthetic history
├── notebooks/            EDA / forecasting / redistribution analysis
├── scripts/              Data generator and optional matplotlib charts
├── tests/                API, ML-feature and safety-match tests
├── docs/assets/          Ten distinct original SVG project visuals
├── docs/                 Architecture, workflows, safety, data and deployment
├── portfolio/            Static portfolio case study
├── powerbi/              Report blueprint + DAX
└── .github/workflows/    Backend and frontend CI
```

## Demo reservation integrity and event log

Cross-listing recipient reservations are capacity-checked under a recipient write lock, and donation cancellations/confirmations are conditional state transitions. New recipients cannot self-verify; a local administrator can mark only fictional recipients using an explicit `DEMO_ADMIN_KEY` (not a production certification). A non-immutable educational event log is available at `GET /api/v1/audit`. See [reservation integrity design](docs/RESERVATION_INTEGRITY.md).

**Latest CI:** The repository's reservation, capacity, demo-verification and audit checks now raise the Python test count to **32 passed**, with frontend and static asset jobs passing. [Verified GitHub run](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40652286477). The API treats new local listings as demo records; simulated pickup counts are not real donations.

## Reproducible database migrations

An Alembic initial revision now provisions the four demo tables in a new database. GitHub CI tests fresh schema creation, reapplying the migration and rollback using disposable SQLite files. This is not a migration of an existing partner database or an independently validated PostgreSQL installation. See [Database migrations](docs/DATABASE_MIGRATIONS.md).

## Featured in the main developer portfolio

FoodBridge AI now appears as a highlighted project and searchable Full Stack card in the existing [Harshavardhan developer portfolio](https://harshakavali81-collab.github.io/harshavardhan-portfolio/).

- [Read the dedicated case study](https://harshakavali81-collab.github.io/harshavardhan-portfolio/cases/foodbridge.html)
- [Explore the portfolio's GitHub source](https://github.com/harshakavali81-collab/harshavardhan-portfolio/blob/main/cases/foodbridge.html)
- [Try the standalone synthetic browser demo](https://harshakavali81-collab.github.io/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/demo.html)

CI on the source repository passed **34 Python tests** with a successful React build and pages deployment on 28 October 2026. Public site showcases remain synthetic and educational; real food redistribution is not certified.

## API highlights
```text
GET  /api/v1/health
GET  /api/v1/dashboard
GET  /api/v1/inventory
POST /api/v1/inventory
GET  /api/v1/recipients
POST /api/v1/recipients
GET  /api/v1/matches/{inventory_id}
POST /api/v1/donations
POST /api/v1/donations/{id}/confirm
POST /api/v1/donations/{id}/cancel
GET  /api/v1/analytics/trends
GET  /api/v1/analytics/export.csv
GET  /api/v1/forecast/preview
```

The `X-API-Key` option gates write operations if configured. It is **not sufficient production authentication** and should never be treated as tenant-level user management.

## Responsible release status

[Launch-readiness status page](docs/launch-readiness.html) clearly separates tested source code, Pages activation, the synthetic interactive demo, and unavailable real-world operating permissions. Static link/asset validation now runs in CI. The [34-test CI run](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40652286477) passed; the [custom GitHub Pages deployment](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40648780305) subsequently succeeded on retry after the owner enabled Pages. Neither GitHub Actions nor a portfolio preview certifies real-food safety.

## Portfolio static hosting

The public static bundle contains [an interactive synthetic demonstration](docs/demo.html) where visitors can filter fictional inventory and simulate reservations without a backend, personal data, or actual donations. It is explicitly *not* the production React/FastAPI app.

**Public site is published according to GitHub Pages:** [Open FoodBridge AI Portfolio](https://harshakavali81-collab.github.io/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/) · [Try the interactive synthetic demo](https://harshakavali81-collab.github.io/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/demo.html) · [Release readiness](https://harshakavali81-collab.github.io/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/launch-readiness.html). The owner enabled Pages on 28 October 2026 and the [dedicated deploy workflow succeeded on its retry](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40648780305). The public website is static; it does not deploy the React/FastAPI backend, connect to real organizations or authorize food distribution.

## Closed, hardened staging environment

This repository also includes a **PostgreSQL API-only staging configuration**. In `APP_ENV=production`, it rejects operational writes even with a service key; reads require a strong server-only key, no demo records are seeded, and startup checks reject unsafe settings. The local React demo is NOT public production authentication. See [deployment commands and remaining release gates](docs/DEPLOYMENT.md), [security readiness](docs/SECURITY_READINESS.md), and [human partner/food-safety onboarding](docs/FOOD_SAFETY_AND_ONBOARDING.md).

## Documentation & portfolio
[Portfolio case study](portfolio/index.html) · [Architecture/ERD](docs/ARCHITECTURE.md) · [Project workflow](docs/PROJECT_WORKFLOW.md) · [Data dictionary](docs/DATA_DICTIONARY.md) · [Safety/limitations](docs/SAFETY_AND_LIMITATIONS.md) · [Deployment checklist](docs/DEPLOYMENT.md) · [Power BI](powerbi/README.md)

**Research source:** [FAO Food Loss and Waste Database](https://www.fao.org/platform-food-loss-waste/flw-data) is a source of published studies, **not** live donor inventory.

**Verified GitHub CI (2026-10-28):** 34 backend tests passed, model training/evaluation completed on synthetic data (MAE 3.908 kg vs 5.49 kg lag-7), static asset checks succeeded, and React production build succeeded. [Verified run](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40652286477). GitHub Pages and an actual public backend are **not deployed**, and no real partners or food safety operations have been verified.

---
Developed as an AI / ML, Python, SQL and full-stack portfolio project · © 2026 · MIT License.
