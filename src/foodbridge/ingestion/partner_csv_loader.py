"""Validate operational CSV separately from published FAO research."""
import pandas as pd
REQUIRED={"date","partner","category","prepared_kg","sold_kg","surplus_kg","donated_kg"}
def load_partner_csv(path):
    df=pd.read_csv(path)
    missing=REQUIRED-set(df.columns)
    if missing:raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["date"]=pd.to_datetime(df["date"],errors="raise")
    for col in ("prepared_kg","sold_kg","surplus_kg","donated_kg"):
        df[col]=pd.to_numeric(df[col],errors="raise")
        if df[col].isna().any() or (df[col]<0).any():raise ValueError(f"Invalid negative or null values: {col}")
    if (df["donated_kg"]>df["surplus_kg"]).any():raise ValueError("Donated exceeds surplus")
    if (df["sold_kg"]+df["surplus_kg"]>df["prepared_kg"]+1e-5).any():raise ValueError("Sold + surplus exceeds prepared")
    if df[["date","partner","category"]].duplicated().any():raise ValueError("Duplicate daily partner/category")
    return df.sort_values(["partner","category","date"]).reset_index(drop=True)
