# Data dictionary

![Lineage](assets/06-data-lineage.svg)

Daily synthetic operations: `date` date, `partner_id` fictitious identifier, `category` food type, `prepared_kg` prepared amount, `sold_kg` sales, `surplus_kg` historical excess, `donated_kg` simulated donations (not confirmed actual collection).

Operational relational tables: `inventory` (food, expiry, allergens, safety acknowledgment, location, allocated quantity), `recipients` (demo verification, storage, categories, capacity, location), `donations` (reservation quantity, lifecycle status, human confirmation).

FAO research data is for separate analysis only and never populates active listings.
