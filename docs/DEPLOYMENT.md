# Deployment guide — public portfolio + closed internal staging

This repository deliberately separates a **public informational portfolio website** from an **internal API-only staging service**. It is not approved for receiving or distributing real food.

## A. GitHub Pages public portfolio

A verified GitHub Actions workflow is in `.github/workflows/pages.yml`. On changes to `docs/`, it uploads ONLY `docs/index.html` and the 10 original SVG visuals. It does not upload .env, partner records, model artifacts or backend sources to the website.

### One-time owner action
1. Open [Repository Settings → Pages](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/settings/pages).
2. Select **Build and deployment → Source: GitHub Actions**.
3. Run **Actions → Deploy portfolio website → Run workflow** if required.
4. Verify the returned URL with `curl -I` or your browser and check that diagrams load.
5. If the action fails before this setting exists, the connected GitHub app cannot grant itself additional Pages administrative permissions.

**Do not claim the website is live until the deployment job succeeds and the URL returns HTTP 200.**

## B. Internal server-side staging using PostgreSQL

This deliberately **disables all inventory, partner and donation mutations**, and requires a server-only API key for operational reads. It does not create public user accounts.

Use on an isolated developer server with Docker Compose and Python available. Do not expose port 8000 to the Internet.

```bash
cp .env.production.example .env.staging
# Set POSTGRES_PASSWORD and API_KEY to independently generated strong, URL-safe secrets
# For example: python -c "import secrets; print(secrets.token_hex(32))"
# Never commit .env.staging or put the API_KEY into browser JavaScript.
docker compose --env-file .env.staging -f docker-compose.staging.yml build
docker compose --env-file .env.staging -f docker-compose.staging.yml up -d db
docker compose --env-file .env.staging -f docker-compose.staging.yml run --rm api python scripts/init_schema_for_staging.py
docker compose --env-file .env.staging -f docker-compose.staging.yml up -d
curl -fsS http://127.0.0.1:8000/api/v1/ready
# Without X-API-Key, inventory endpoints must return HTTP 401.
# With the server-side key, inventory initially returns [].
```

The `scripts/init_schema_for_staging.py` bootstrap is suitable for a **fresh empty, isolated staging database only**. Later schema evolution requires Alembic migrations and reviewed changes. The PostgreSQL container uses a persistent volume, unexposed DB port, dedicated internal network and container health checks; API is bound to localhost.

Never configure a public frontend with the shared API key. The React UI remains a **local educational demo only** and uses no privileged browser-stored credentials.

## Production release gates

1. Independently verify donor and recipient registration, formal consent, authority to collect, trained handlers and distribution operations.
2. Build a secure multi-user identity layer (OIDC + server sessions + RBAC), tenant isolation for every DB query, and field-level privacy decisions.
3. Complete a human-run food safety procedure and immutable evidence for temperature, allergen, packaging, recalls, time and transport.
4. Implement reversible database migrations, tested backups/restores, encryption, monitoring, rate limiting, secrets rotation, and incident response.
5. Obtain a domain/TLS, hosting account with billing agreement, database backup policy, tested staging-to-prod promotion.
6. Pilot only with explicitly authorized partners and validated real data; calibrate forecasting by partner and verify results.

Until those gates are met, the backend **intentionally refuses all operational writes in production**.

See [Safety & onboarding](FOOD_SAFETY_AND_ONBOARDING.md), [Security readiness](SECURITY_READINESS.md), and [FSSAI surplus food regulations](https://www.fssai.gov.in/food-law/regulations).
