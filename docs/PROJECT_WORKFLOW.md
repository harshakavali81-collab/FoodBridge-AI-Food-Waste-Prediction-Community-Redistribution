# Project workflow

![Workflow](assets/03-redistribution-workflow.svg)
![Matching rules](assets/04-matching-decision-tree.svg)
![Forecast steps](assets/05-forecasting-pipeline.svg)

1. Generate synthetic history or validate permissioned partner input.
2. Run EDA and past-only lag feature engineering.
3. Split chronologically and compare a model against the naive baseline.
4. Explicitly record actually available inventory with donor safety review.
5. Screen recipient verification, storage, category, capacity, time and distance.
6. Atomically reserve inventory, then either cancel or confirm actual pickup.
7. Report predicted, listed, reserved and confirmed quantities separately.

**Not implemented for production:** independently verified charity onboarding, cold-chain monitoring, driving routes, user tenancy, live data validation or environmental impact certification.
