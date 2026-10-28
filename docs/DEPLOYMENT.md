# Deployment checklist

## Local demo
```bash
cp .env.example .env
docker compose up --build
```

The demo services listen on localhost; configure `API_KEY` for write access when appropriate.

## Real-world deployment requires
HTTPS, account authentication and role permissions; independently verified partners; temperature and recall processes; tenant-isolated storage; secret management; backups and migrations; audit logging; rate limits; privacy compliance; accessibility audits; independent model validation; and secure hosting. **None of those are claimed complete.**
