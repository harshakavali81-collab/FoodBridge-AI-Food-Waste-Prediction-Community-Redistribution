from pathlib import Path
import pandas as pd
from foodbridge.processing.features import make_features
from foodbridge.ingestion.partner_csv_loader import load_partner_csv
from foodbridge.forecasting.evaluate import metrics
def test_past_only_features():
    df=pd.DataFrame({"partner":["P"]*12,"category":["bakery"]*12,"date":pd.date_range("2026-01-01",periods=12),"surplus_kg":list(range(12))})
    f=make_features(df);assert len(f)==5
    row=f[f.surplus_kg==7].iloc[0]
    assert row.lag_1==6 and row.lag_7==0 and row.rolling_7==3
def test_metrics():
    assert metrics([1,2],[1,3])["mae_kg"]==.5
def test_sample_data():
    csv=Path(__file__).parents[1]/"data/synthetic/daily_operations.csv"
    df=load_partner_csv(csv)
    assert len(df)==840
    assert (df.donated_kg<=df.surplus_kg).all()
