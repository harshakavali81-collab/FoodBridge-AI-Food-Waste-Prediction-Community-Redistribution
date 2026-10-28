# Power BI report blueprint

Source: `data/synthetic/daily_operations.csv` (synthetic only).

Suggested report pages:
1. **Operations:** prepared, sold, surplus and simulated donated kg by partner.
2. **Category trends:** daily and weekly charts with date and food category slicers.
3. **Model validation:** read `models/evaluation.json` after training, compare baseline and Random Forest error.
4. **Donation audit:** operational `donations` records exported from authorized local database; only collected is a confirmed pickup.

DAX example:
```dax
Surplus Kg = SUM(daily_operations[surplus_kg])
Simulated Donation Kg = SUM(daily_operations[donated_kg])
Surplus Rate = DIVIDE([Surplus Kg], SUM(daily_operations[prepared_kg]))
```
**Caution:** `donated_kg` in synthetic history is simulated, not verified collections.
