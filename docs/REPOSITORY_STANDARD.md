# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile.api`](<../Dockerfile.api>)
- [`Dockerfile.staging`](<../Dockerfile.staging>)
- [`LICENSE`](<../LICENSE>)
- [`README.md`](<../README.md>)
- [`SECURITY.md`](<../SECURITY.md>)
- [`alembic.ini`](<../alembic.ini>)
- [`backend`](<../backend>)
- [`backend/__init__.py`](<../backend/__init__.py>)
- [`backend/app`](<../backend/app>)
- [`backend/app/__init__.py`](<../backend/app/__init__.py>)
- [`backend/app/db`](<../backend/app/db>)
- [`backend/app/db/__init__.py`](<../backend/app/db/__init__.py>)
- [`backend/app/db/database.py`](<../backend/app/db/database.py>)
- [`backend/app/db/models.py`](<../backend/app/db/models.py>)
- [`backend/app/db/seed.py`](<../backend/app/db/seed.py>)
- [`backend/app/identity.py`](<../backend/app/identity.py>)
- [`backend/app/main.py`](<../backend/app/main.py>)
- [`backend/app/routes`](<../backend/app/routes>)
- [`backend/app/routes/__init__.py`](<../backend/app/routes/__init__.py>)
- [`backend/app/routes/analytics.py`](<../backend/app/routes/analytics.py>)
- [`backend/app/routes/audit.py`](<../backend/app/routes/audit.py>)
- [`backend/app/routes/donations.py`](<../backend/app/routes/donations.py>)
- [`backend/app/routes/inventory.py`](<../backend/app/routes/inventory.py>)
- [`backend/app/routes/pilot.py`](<../backend/app/routes/pilot.py>)
- [`backend/app/routes/recipients.py`](<../backend/app/routes/recipients.py>)
- [`backend/app/schemas.py`](<../backend/app/schemas.py>)
- [`backend/app/security.py`](<../backend/app/security.py>)
- [`data`](<../data>)
- [`data/synthetic`](<../data/synthetic>)
- [`data/synthetic/daily_operations.csv`](<../data/synthetic/daily_operations.csv>)
- [`docker-compose.staging.yml`](<../docker-compose.staging.yml>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/DATABASE_MIGRATIONS.md`](<../docs/DATABASE_MIGRATIONS.md>)
- [`docs/DATA_DICTIONARY.md`](<../docs/DATA_DICTIONARY.md>)
- [`docs/DEPLOYMENT.md`](<../docs/DEPLOYMENT.md>)
- [`docs/FOOD_SAFETY_AND_ONBOARDING.md`](<../docs/FOOD_SAFETY_AND_ONBOARDING.md>)
- [`docs/IDENTITY_AND_PILOT_REVIEWS.md`](<../docs/IDENTITY_AND_PILOT_REVIEWS.md>)
- [`docs/INTEGRITY_AND_RECOVERY.md`](<../docs/INTEGRITY_AND_RECOVERY.md>)
- [`docs/PROJECT_WORKFLOW.md`](<../docs/PROJECT_WORKFLOW.md>)
- [`docs/RESERVATION_INTEGRITY.md`](<../docs/RESERVATION_INTEGRITY.md>)
- [`docs/SAFETY_AND_LIMITATIONS.md`](<../docs/SAFETY_AND_LIMITATIONS.md>)
- [`docs/SECURITY_READINESS.md`](<../docs/SECURITY_READINESS.md>)
- [`docs/assets`](<../docs/assets>)
- [`docs/assets/01-hero-banner.svg`](<../docs/assets/01-hero-banner.svg>)
- [`docs/assets/02-system-architecture.svg`](<../docs/assets/02-system-architecture.svg>)
- [`docs/assets/03-redistribution-workflow.svg`](<../docs/assets/03-redistribution-workflow.svg>)
- [`docs/assets/04-matching-decision-tree.svg`](<../docs/assets/04-matching-decision-tree.svg>)
- [`docs/assets/05-forecasting-pipeline.svg`](<../docs/assets/05-forecasting-pipeline.svg>)
- [`docs/assets/06-data-lineage.svg`](<../docs/assets/06-data-lineage.svg>)
- [`docs/assets/07-model-comparison.svg`](<../docs/assets/07-model-comparison.svg>)
- [`docs/assets/08-surplus-trends.svg`](<../docs/assets/08-surplus-trends.svg>)
- [`docs/assets/09-category-mix.svg`](<../docs/assets/09-category-mix.svg>)
- [`docs/assets/10-impact-funnel.svg`](<../docs/assets/10-impact-funnel.svg>)
- [`docs/demo.html`](<../docs/demo.html>)
- [`docs/index.html`](<../docs/index.html>)
- [`docs/launch-readiness.html`](<../docs/launch-readiness.html>)
- [`frontend`](<../frontend>)
- [`frontend/Dockerfile`](<../frontend/Dockerfile>)
- [`frontend/index.html`](<../frontend/index.html>)
- [`frontend/nginx.conf`](<../frontend/nginx.conf>)
- [`frontend/package.json`](<../frontend/package.json>)
- [`frontend/src`](<../frontend/src>)
- [`frontend/src/api`](<../frontend/src/api>)
- [`frontend/src/api/client.js`](<../frontend/src/api/client.js>)
- [`frontend/src/components`](<../frontend/src/components>)
- [`frontend/src/components/Sidebar.jsx`](<../frontend/src/components/Sidebar.jsx>)
- [`frontend/src/components/UI.jsx`](<../frontend/src/components/UI.jsx>)
- [`frontend/src/main.jsx`](<../frontend/src/main.jsx>)
- [`frontend/src/pages`](<../frontend/src/pages>)
- [`frontend/src/pages/Analytics.jsx`](<../frontend/src/pages/Analytics.jsx>)
- [`frontend/src/pages/Dashboard.jsx`](<../frontend/src/pages/Dashboard.jsx>)
- [`frontend/src/pages/Donations.jsx`](<../frontend/src/pages/Donations.jsx>)
- [`frontend/src/pages/RecipientMatches.jsx`](<../frontend/src/pages/RecipientMatches.jsx>)
- [`frontend/src/pages/Recipients.jsx`](<../frontend/src/pages/Recipients.jsx>)
- [`frontend/src/pages/Surplus.jsx`](<../frontend/src/pages/Surplus.jsx>)
- [`frontend/src/style.css`](<../frontend/src/style.css>)
- [`frontend/vite.config.js`](<../frontend/vite.config.js>)
- [`migrations`](<../migrations>)
- [`migrations/env.py`](<../migrations/env.py>)
- [`migrations/script.py.mako`](<../migrations/script.py.mako>)
- [`migrations/versions`](<../migrations/versions>)
- [`migrations/versions/20261028_01_initial_schema.py`](<../migrations/versions/20261028_01_initial_schema.py>)
- [`migrations/versions/20261028_02_pilot_readiness.py`](<../migrations/versions/20261028_02_pilot_readiness.py>)
- [`notebooks`](<../notebooks>)
- [`notebooks/01_surplus_eda.ipynb`](<../notebooks/01_surplus_eda.ipynb>)
- [`notebooks/02_demand_forecast.ipynb`](<../notebooks/02_demand_forecast.ipynb>)
- [`notebooks/03_redistribution_analysis.ipynb`](<../notebooks/03_redistribution_analysis.ipynb>)
- [`portfolio`](<../portfolio>)
- [`portfolio/CASE_STUDY.md`](<../portfolio/CASE_STUDY.md>)
- [`portfolio/index.html`](<../portfolio/index.html>)
- [`powerbi`](<../powerbi>)
- [`powerbi/README.md`](<../powerbi/README.md>)
- [`pytest.ini`](<../pytest.ini>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/check_deployment.py`](<../scripts/check_deployment.py>)
- [`scripts/check_inventory_integrity.py`](<../scripts/check_inventory_integrity.py>)
- [`scripts/generate_synthetic.py`](<../scripts/generate_synthetic.py>)
- [`scripts/init_schema_for_staging.py`](<../scripts/init_schema_for_staging.py>)
- [`scripts/make_visuals_and_notebooks.py`](<../scripts/make_visuals_and_notebooks.py>)
- [`scripts/verify_backup_restore_ci.py`](<../scripts/verify_backup_restore_ci.py>)
- [`src`](<../src>)
- [`src/__init__.py`](<../src/__init__.py>)
- [`src/foodbridge`](<../src/foodbridge>)
- [`src/foodbridge/__init__.py`](<../src/foodbridge/__init__.py>)
- [`src/foodbridge/forecasting`](<../src/foodbridge/forecasting>)
- [`src/foodbridge/forecasting/__init__.py`](<../src/foodbridge/forecasting/__init__.py>)
- [`src/foodbridge/forecasting/evaluate.py`](<../src/foodbridge/forecasting/evaluate.py>)
- [`src/foodbridge/forecasting/predict_surplus.py`](<../src/foodbridge/forecasting/predict_surplus.py>)
- [`src/foodbridge/forecasting/train.py`](<../src/foodbridge/forecasting/train.py>)
- [`src/foodbridge/ingestion`](<../src/foodbridge/ingestion>)
- [`src/foodbridge/ingestion/__init__.py`](<../src/foodbridge/ingestion/__init__.py>)
- [`src/foodbridge/ingestion/fao_research_loader.py`](<../src/foodbridge/ingestion/fao_research_loader.py>)
- [`src/foodbridge/ingestion/partner_csv_loader.py`](<../src/foodbridge/ingestion/partner_csv_loader.py>)
- [`src/foodbridge/matching`](<../src/foodbridge/matching>)
- [`src/foodbridge/matching/__init__.py`](<../src/foodbridge/matching/__init__.py>)
- [`src/foodbridge/matching/eligibility.py`](<../src/foodbridge/matching/eligibility.py>)
- [`src/foodbridge/matching/match_donations.py`](<../src/foodbridge/matching/match_donations.py>)
- [`src/foodbridge/matching/route_cost.py`](<../src/foodbridge/matching/route_cost.py>)
- [`src/foodbridge/monitoring`](<../src/foodbridge/monitoring>)
- [`src/foodbridge/monitoring/__init__.py`](<../src/foodbridge/monitoring/__init__.py>)
- [`src/foodbridge/monitoring/ledger.py`](<../src/foodbridge/monitoring/ledger.py>)
- [`src/foodbridge/monitoring/quality_report.py`](<../src/foodbridge/monitoring/quality_report.py>)
- [`src/foodbridge/processing`](<../src/foodbridge/processing>)
- [`src/foodbridge/processing/__init__.py`](<../src/foodbridge/processing/__init__.py>)
- [`src/foodbridge/processing/clean.py`](<../src/foodbridge/processing/clean.py>)
- [`src/foodbridge/processing/features.py`](<../src/foodbridge/processing/features.py>)
- [`src/foodbridge/processing/validation.py`](<../src/foodbridge/processing/validation.py>)
- [`tests`](<../tests>)
- [`tests/conftest.py`](<../tests/conftest.py>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_deployment_security.py`](<../tests/test_deployment_security.py>)
- [`tests/test_forecasting.py`](<../tests/test_forecasting.py>)
- [`tests/test_integrity_ledger.py`](<../tests/test_integrity_ledger.py>)
- [`tests/test_matching.py`](<../tests/test_matching.py>)
- [`tests/test_migrations.py`](<../tests/test_migrations.py>)
- [`tests/test_pilot_identity.py`](<../tests/test_pilot_identity.py>)
- [`tests/test_postgres_integration.py`](<../tests/test_postgres_integration.py>)
- [`tests/test_reservation_integrity.py`](<../tests/test_reservation_integrity.py>)
- [`tests/test_site_integrity.py`](<../tests/test_site_integrity.py>)
