# Signed identity and pilot-readiness sandbox — not real authorization

## Security boundaries

- `GET /api/v1/identity/me` verifies a signed RS256 JWT using a preconfigured identity provider's **public key**. Verifies `iss`, `aud`, `iat`, `exp`, `sub`, requires a syntactically valid `tenant_id` and one of `operator`, `reviewer`, `auditor`, `admin` roles.
- Identity routes are fail-closed without `OIDC_PUBLIC_KEY_PEM`, `OIDC_ISSUER`, `OIDC_AUDIENCE`. Production API's preexisting internal service key remains required for all non-health routes. This is NOT a public browser login flow.
- **Reviewer** can record `demo:`-only references on eight mock checks. The tenant is always taken from a **signed token**, not from the request body or a caller-supplied header. The review record is tenant-scoped.
- **Auditor, operator, reviewer, admin** may view only their token's tenant readiness data.
- **Admin** can request a readiness *simulation*; it needs all eight mock checks accepted and evidence of at least two different reviewer token subjects. The response explicitly includes `authorized_for_real_distribution: false` even if all are fulfilled.
- **All pilot-review writes are rejected in production**, and every other operational write remains disabled.
- No raw sensitive documents or real beneficiary details are accepted. `evidence_ref` must be a fictional value like `demo:temperature-check`.
- The event log is a prototype, not cryptographically immutable legal evidence.

## API surface

```text
GET  /api/v1/identity/me         signed Bearer JWT
GET  /api/v1/pilot/readiness    tenant-scoped Bearer JWT
POST /api/v1/pilot/reviews      reviewer, demo-only, JSON check_key/status/evidence_ref
POST /api/v1/pilot/evaluate     admin, demo-only; NEVER authorizes real pilot
```

## Auth configuration example (no secrets)

```bash
OIDC_ISSUER=https://identity.example.org/
OIDC_AUDIENCE=foodbridge-internal
OIDC_PUBLIC_KEY_PEM="-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----"
```

Use a genuine organization-controlled identity provider for real identity verification, key rotation and secure multiuser onboarding. **This source alone does not create accounts, SSO, consent, permissioned access to actual food records, or secure tenant isolation for the pre-existing inventory tables.**

## Separately required production gates

1. Authorize a hosting provider, DNS and TLS, egress restrictions and a managed PostgreSQL database.
2. Integrate a real OIDC provider with rotating JWKS and revocation/session policies. Independent penetration testing and threat modeling required.
3. Partition inventory, recipients, donations and audit rows by authenticated tenant and enforce authorization on every query (current records are still demo-only and unscoped).
4. Independently verify donor/recipient legal status, food handling, temperature equipment and compliance obligations. Obtain a trained domain expert's written approval.
5. Establish authentic human pickup confirmations and a recall/complaint escalation process.
6. Obtain an actual signed pilot agreement and assign responsible operations staff; never infer permission from a software checklist.

## PostgreSQL verification

A disposable PostgreSQL 17 service is provisioned in GitHub Actions. CI applies Alembic revisions, verifies the table/foreign-key structure, confirms cross-tenant uniqueness for mock reviews, re-runs schema setup, and destroys the isolated runner afterward. This does **not** prove production row-level security, secure real user accounts, backups, a public database, or a deployed food service.
