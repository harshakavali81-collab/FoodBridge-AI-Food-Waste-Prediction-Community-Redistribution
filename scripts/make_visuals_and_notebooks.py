"""Build additional optional static matplotlib figures from the synthetic dataset."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def main():
    df=pd.read_csv("data/synthetic/daily_operations.csv")
    df["date"]=pd.to_datetime(df["date"])
    out=Path("docs/generated");out.mkdir(parents=True,exist_ok=True)
    daily=df.groupby("date")[["surplus_kg","donated_kg"]].sum()
    ax=daily.plot(figsize=(11,5),title="Synthetic surplus and simulated donations")
    ax.set_ylabel("Kg (synthetic)");plt.tight_layout();plt.savefig(out/"synthetic-trends.png",dpi=160);plt.close()
    cat=df.groupby("category")["surplus_kg"].sum().sort_values().plot(kind="barh",title="Synthetic category surplus")
    cat.set_xlabel("Kg (synthetic)");plt.tight_layout();plt.savefig(out/"category-chart.png",dpi=160);plt.close()
if __name__=="__main__":main()
