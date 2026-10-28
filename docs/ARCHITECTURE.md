# System architecture

![Architecture](assets/02-system-architecture.svg)

```mermaid
flowchart LR
  UI[React UI] --> API[FastAPI]
  API --> DB[(SQLite / PostgreSQL)]
  API --> Rules[Eligibility rules]
  CSV[Synthetic history] --> Features[Past-only features]
  Features --> ML[Chronological model evaluation]
  CSV --> BI[Analytics & Power BI]
```

```mermaid
erDiagram
 INVENTORY ||--o{ DONATIONS : allocated
 RECIPIENTS ||--o{ DONATIONS : receives
 AUDIT_EVENTS { int id PK string event_type string entity_type int entity_id datetime created_at }
 INVENTORY { int id PK float quantity_kg float allocated_kg datetime expires_at }
 RECIPIENTS { int id PK float capacity_kg bool verified }
 DONATIONS { int id PK int inventory_id FK int recipient_id FK string status }
```

ML predictions are separate from operational listings. FAO publications are a research source, not live inventory.


Donation reservations additionally lock a recipient row and re-check capacity against the sum of active reservations, to avoid oversubscribing a recipient across multiple inventory listings. See [Reservation integrity](RESERVATION_INTEGRITY.md).
