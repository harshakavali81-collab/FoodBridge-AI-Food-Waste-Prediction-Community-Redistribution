# Security readiness review

## Implemented in this repository
- Production startup validates minimum 32-character API key, PostgreSQL URL, no demo seeding and HTTPS-only/empty CORS allowlist.
- Production read endpoints require a server-to-server key. **All production operational writes are denied** regardless of key.
- API security headers, readiness check, localhost-only internal Docker staging port, PostgreSQL-only internal network.
- Staging container uses unprivileged user; no browser access to server-side API key; `.env.staging` excluded from Git.
- GitHub Actions builds/tests and static Pages workflow includes only portfolio HTML/SVG.
- Demo route eligibility rejects expired stock, missing acknowledgment, nonverified recipients and storage/capacity mismatch.

## Not implemented — block production release
- OIDC/SSO user identities, secure browser sessions, CSRF strategy, per-organization roles and access policies.
- Tenant isolation for all data reads and writes, authorization tests and independent penetration review.
- Actual independent partner identity verification and authorized food-handling sign-offs.
- Immutable audit trails, secure document storage, recall/complaint process and traceability review.
- GDPR/DPDP applicability review, data retention, deletion and breach escalation.
- CI dependency vulnerability handling, CI supply-chain pinning and independently tested backup restoration.
- Alembic initial schema creation is now tested on disposable SQLite, but PostgreSQL migration behavior, ongoing real-data schema upgrades, high availability, public HTTPS, managed observability and SLOs remain unverified.
- Independent external model validation using reliable real operational history.

## Explicit threat boundaries
Do not reuse the demo's API key as user login; it is only an internal service secret. Do not expose the internal API directly to the Internet, copy credentials to JavaScript, or allow public writes. The API's generic database tables are NOT tenant-aware: keep all data fictional and do not ingest beneficiary personal details.

Incident response before real deployment must define owner, intake address, classification and response timetable.

For confidential vulnerability reports, use GitHub's private vulnerability reporting if enabled, or contact the repository maintainer through a secure private channel. Do not open public issues containing security details.

## Additional cryptographic identity demo (2026-10-28)

A non-operational, tenant-scoped review sandbox validates RS256 JWT signatures and issuer/audience/time claims, enforces demo roles and tenant scoping on `pilot_reviews`, and requires two distinct reviewers for an all-checks-complete simulation. See [identity and pilot reviews](IDENTITY_AND_PILOT_REVIEWS.md). Production writes remain disabled, and legacy inventory/donation tables are **not tenant-scoped**. Token validation alone does not constitute a production identity system.

## Verified disposable PostgreSQL schema checks (2026-10-28)

[GitHub CI run](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40654758756) passed PostgreSQL 17 service tests against initial + second Alembic migrations, tenant-review uniqueness, and donation foreign keys. The integration test intentionally triggers a duplicate-key rejection and confirms the database enforces it. This is isolated CI evidence, **not** an audited production database or row-level security for donations.
