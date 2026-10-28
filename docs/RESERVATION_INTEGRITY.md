# Concurrent reservation and audit demonstration

## Why this was added

Checking an individual recipient's total capacity against one request is insufficient: the same recipient might be booked for multiple listings, causing overbooking.

**Updated demo design** (PostgreSQL READ COMMITTED, SQLite single-writer semantics):
1. Check safety, expiry, category, distance and quantity before writing.
2. Acquire the recipient's database write lock with a no-op row update.
3. Calculate recipient's outstanding **reserved** donation kilograms under the lock.
4. Reject if request exceeds `capacity_kg - sum(reserved)`.
5. Atomically increase inventory allocated kilograms only when sufficient stock and valid dates still hold.
6. Create the donation and a demo event in the **same transaction**.
7. Confirmation or cancellation changes only a **reserved** donation, rejects duplicate transitions, and releases recipient capacity. Cancellation also releases inventory stock.
8. Match previews take active recipient reservations into account.

The audit log is a local append-only-in-application example; it is **not tamper-proof**, signed, or a regulatory chain of custody.

## Real-world boundary

Recipients must be independently verified under applicable law and safety review. API-submitted new recipients start unverified. A **separate local-only** `/api/v1/recipients/{id}/verify-demo` endpoint (with `DEMO_ADMIN_KEY`, min 16 characters, rejected in APP_ENV=production) supports repeatable fictional scenarios and is not an approval of a real charity.

Inventory and donations remain enabled only in development demo mode. Production operational writes are still always rejected, regardless of credentials.

## Database evolution

An `audit_events` table is created by existing local demo `Base.metadata.create_all` at startup. Existing table structures are not changed. Production staging requires audited schema migrations and external identity/tenant controls before use.

## Evidence

`tests/test_reservation_integrity.py` covers recipient overbooking, rejection of self-verified partners, internal-only demo verification, release of reserved capacity, duplicate cancellation and audit events. GitHub Actions provides independently reproducible CI build evidence; it does not certify physical food handling.
