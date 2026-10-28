"""No label leakage: all rolling/lagged data are shifted one day or more."""
import pandas as pd
CATEGORICAL=["partner","category"]
NUMERICAL=["weekday","month","lag_1","lag_7","rolling_7"]
FEATURES=CATEGORICAL+NUMERICAL
def make_features(df:pd.DataFrame)->pd.DataFrame:
    rows=df.sort_values(["partner","category","date"]).copy()
    rows["date"]=pd.to_datetime(rows["date"])
    rows["weekday"]=rows["date"].dt.dayofweek;rows["month"]=rows["date"].dt.month
    group=rows.groupby(["partner","category"],sort=False)["surplus_kg"]
    rows["lag_1"]=group.shift(1);rows["lag_7"]=group.shift(7)
    rows["rolling_7"]=rows.groupby(["partner","category"],sort=False)["surplus_kg"].transform(lambda x:x.shift(1).rolling(7,min_periods=7).mean())
    return rows.dropna(subset=["lag_1","lag_7","rolling_7"]).sort_values("date").reset_index(drop=True)
